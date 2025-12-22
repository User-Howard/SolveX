from __future__ import annotations

from psycopg import Connection

from src.api import schemas
from src.api.routes.utils import get_problem_with_author


def build_problem_full(conn: Connection, problem_id: int) -> schemas.ProblemFull:
    # 1. Get problem with author
    problem_data = get_problem_with_author(conn, problem_id)

    # 2. Get solutions
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM solutions
            WHERE problem_id = %s
            ORDER BY created_at DESC
            """,
            (problem_id,),
        )
        solutions = [schemas.SolutionRead.model_validate(r) for r in cur.fetchall()]

    # 3. Get tags
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT t.* FROM tags t
            JOIN problem_tags pt ON t.tag_id = pt.tag_id
            WHERE pt.problem_id = %s
            """,
            (problem_id,),
        )
        tags = [schemas.TagRead.model_validate(r) for r in cur.fetchall()]

    # 4. Get linked resources with metadata
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                r.*,
                pr.relevance_score,
                pr.contribution_type
            FROM resources r
            JOIN problem_resources pr ON r.resource_id = pr.resource_id
            WHERE pr.problem_id = %s
            """,
            (problem_id,),
        )
        linked_resources = [
            schemas.ProblemResourceSummary(
                resource=schemas.ResourceRead.model_validate(r),
                relevance_score=r["relevance_score"],
                contribution_type=r["contribution_type"],
            )
            for r in cur.fetchall()
        ]

    # 5. Get outward relations
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM problem_relations
            WHERE from_problem_id = %s
            """,
            (problem_id,),
        )
        relations_out = [schemas.ProblemRelationRead.model_validate(r) for r in cur.fetchall()]

    # 6. Get inward relations
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM problem_relations
            WHERE to_problem_id = %s
            """,
            (problem_id,),
        )
        relations_in = [schemas.ProblemRelationRead.model_validate(r) for r in cur.fetchall()]

    return schemas.ProblemFull(
        problem=schemas.ProblemWithAuthor.model_validate(problem_data),
        solutions=solutions,
        tags=tags,
        linked_resources=linked_resources,
        relations_out=relations_out,
        relations_in=relations_in,
    )
