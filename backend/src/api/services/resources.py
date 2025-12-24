from __future__ import annotations

from psycopg import Connection

from src.api import schemas
from src.api.routes.utils import get_resource_or_404


def build_resource_detail(conn: Connection, resource_id: int) -> schemas.ResourceDetail:
    # 1. Get resource
    resource = get_resource_or_404(conn, resource_id)

    # 2. Get linked problems
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT p.* FROM problems p
            JOIN problem_resources pr ON p.problem_id = pr.problem_id
            WHERE pr.resource_id = %s
            ORDER BY p.created_at DESC
            """,
            (resource_id,),
        )
        linked_problems = [schemas.ProblemListItem.model_validate(r) for r in cur.fetchall()]

    # 3. Get linked solutions
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT s.* FROM solutions s
            JOIN solution_resources sr ON s.solution_id = sr.solution_id
            WHERE sr.resource_id = %s
            ORDER BY s.created_at DESC
            """,
            (resource_id,),
        )
        linked_solutions = [schemas.SolutionRead.model_validate(r) for r in cur.fetchall()]

    # 4. Get tags
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT t.* FROM tags t
            JOIN resource_tags rt ON t.tag_id = rt.tag_id
            WHERE rt.resource_id = %s
            """,
            (resource_id,),
        )
        tags = [schemas.TagRead.model_validate(r) for r in cur.fetchall()]

    return schemas.ResourceDetail(
        **schemas.ResourceRead.model_validate(resource).model_dump(),
        linked_problems=linked_problems,
        linked_solutions=linked_solutions,
        tags=tags,
    )
