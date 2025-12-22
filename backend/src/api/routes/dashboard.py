from fastapi import APIRouter

from src.api import schemas
from src.api.deps import ConnectionDep
from src.api.routes.utils import get_user_or_404


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/{user_id}", response_model=schemas.DashboardResponse)
def get_dashboard(user_id: int, conn: ConnectionDep):
    get_user_or_404(conn, user_id)

    # 1. Get recent problems
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM problems
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 10
            """,
            (user_id,),
        )
        recent_problems = [schemas.ProblemListItem.model_validate(r) for r in cur.fetchall()]

    # 2. Get recent solutions
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT s.* FROM solutions s
            JOIN problems p ON s.problem_id = p.problem_id
            WHERE p.user_id = %s
            ORDER BY s.created_at DESC
            LIMIT 10
            """,
            (user_id,),
        )
        recent_solutions = [schemas.SolutionRead.model_validate(r) for r in cur.fetchall()]

    # 3. Get top tags (LEFT JOIN + GROUP BY)
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                t.tag_id,
                t.tag_name,
                COUNT(pt.problem_id) as usage_count
            FROM tags t
            LEFT JOIN problem_tags pt ON t.tag_id = pt.tag_id
            GROUP BY t.tag_id, t.tag_name
            ORDER BY usage_count DESC
            LIMIT 5
            """
        )
        top_tags = [
            schemas.TopTag(
                tag_id=row["tag_id"],
                tag_name=row["tag_name"],
                usage_count=row["usage_count"] or 0,
            )
            for row in cur.fetchall()
        ]

    # 4. Get top resources (correlated subqueries)
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                r.resource_id,
                r.title,
                (
                    SELECT COUNT(*)
                    FROM problem_resources pr
                    WHERE pr.resource_id = r.resource_id
                ) + (
                    SELECT COUNT(*)
                    FROM solution_resources sr
                    WHERE sr.resource_id = r.resource_id
                ) as usage_count
            FROM resources r
            ORDER BY usage_count DESC
            LIMIT 5
            """
        )
        top_resources = [
            schemas.TopResource(
                resource_id=row["resource_id"],
                title=row["title"],
                usage_count=row["usage_count"] or 0,
            )
            for row in cur.fetchall()
        ]

    return schemas.DashboardResponse(
        recent_problems=recent_problems,
        recent_solutions=recent_solutions,
        top_tags=top_tags,
        top_resources=top_resources,
    )
