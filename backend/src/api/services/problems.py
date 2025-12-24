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
        solution_rows = cur.fetchall()

    resources_by_solution: dict[int, list[schemas.ResourceRead]] = {
        row["solution_id"]: [] for row in solution_rows
    }

    if solution_rows:
        solution_ids = [row["solution_id"] for row in solution_rows]
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT sr.solution_id, r.*
                FROM solution_resources sr
                JOIN resources r ON r.resource_id = sr.resource_id
                WHERE sr.solution_id = ANY(%s)
                ORDER BY r.last_visited_at DESC, r.resource_id DESC
                """,
                (solution_ids,),
            )
            for row in cur.fetchall():
                resource_data = dict(row)
                solution_id = resource_data.pop("solution_id")
                resources_by_solution[solution_id].append(
                    schemas.ResourceRead.model_validate(resource_data)
                )

    solutions = [
        schemas.SolutionWithResources(
            **schemas.SolutionRead.model_validate(row).model_dump(),
            resources=resources_by_solution.get(row["solution_id"], []),
        )
        for row in solution_rows
    ]

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
