from fastapi import APIRouter, HTTPException, status
from psycopg import errors

from src.api import schemas
from src.api.deps import ConnectionDep
from src.api.routes.utils import (
    get_problem_or_404,
    get_resource_or_404,
    get_solution_or_404,
)
from src.api.services.problems import build_problem_full


router = APIRouter(tags=["relations"])


@router.post("/problems/{problem_id}/relations", response_model=schemas.ProblemRelationRead, status_code=status.HTTP_201_CREATED)
def create_problem_relation(problem_id: int, payload: schemas.ProblemRelationCreate, conn: ConnectionDep):
    get_problem_or_404(conn, problem_id)
    get_problem_or_404(conn, payload.to_problem_id)

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO problem_relations (from_problem_id, to_problem_id, relation_type, strength)
                VALUES (%s, %s, %s, %s)
                RETURNING *
                """,
                (problem_id, payload.to_problem_id, payload.relation_type, payload.strength),
            )
            row = cur.fetchone()
        conn.commit()
        return schemas.ProblemRelationRead.model_validate(row)
    except errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Relation already exists")


@router.delete("/problems/{problem_id}/relations/{to_problem_id}")
def delete_problem_relation(problem_id: int, to_problem_id: int, conn: ConnectionDep):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM problem_relations
            WHERE from_problem_id = %s AND to_problem_id = %s
            """,
            (problem_id, to_problem_id),
        )
        relation = cur.fetchone()

    if not relation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relation not found")

    with conn.cursor() as cur:
        cur.execute(
            """
            DELETE FROM problem_relations
            WHERE from_problem_id = %s AND to_problem_id = %s
            """,
            (problem_id, to_problem_id),
        )
    conn.commit()
    return {"deleted": True}


@router.get("/problems/{problem_id}/relations/out", response_model=list[schemas.ProblemRelationRead])
def list_problem_relations_out(problem_id: int, conn: ConnectionDep):
    get_problem_or_404(conn, problem_id)

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM problem_relations
            WHERE from_problem_id = %s
            """,
            (problem_id,),
        )
        rows = cur.fetchall()

    return [schemas.ProblemRelationRead.model_validate(row) for row in rows]


@router.get("/problems/{problem_id}/relations/in", response_model=list[schemas.ProblemRelationRead])
def list_problem_relations_in(problem_id: int, conn: ConnectionDep):
    get_problem_or_404(conn, problem_id)

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM problem_relations
            WHERE to_problem_id = %s
            """,
            (problem_id,),
        )
        rows = cur.fetchall()

    return [schemas.ProblemRelationRead.model_validate(row) for row in rows]


@router.post("/problems/{problem_id}/resources", response_model=schemas.ProblemFull)
def attach_resource_to_problem(problem_id: int, payload: schemas.ProblemResourceAttach, conn: ConnectionDep):
    get_problem_or_404(conn, problem_id)
    get_resource_or_404(conn, payload.resource_id)

    # Check if link exists (upsert pattern)
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM problem_resources
            WHERE problem_id = %s AND resource_id = %s
            """,
            (problem_id, payload.resource_id),
        )
        existing = cur.fetchone()

    if not existing:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO problem_resources (problem_id, resource_id, relevance_score, contribution_type)
                VALUES (%s, %s, %s, %s)
                """,
                (problem_id, payload.resource_id, payload.relevance_score, payload.contribution_type),
            )
    else:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE problem_resources
                SET relevance_score = %s, contribution_type = %s
                WHERE problem_id = %s AND resource_id = %s
                """,
                (payload.relevance_score, payload.contribution_type, problem_id, payload.resource_id),
            )
    conn.commit()
    return build_problem_full(conn, problem_id)


@router.delete("/problems/{problem_id}/resources/{resource_id}", response_model=schemas.ProblemFull)
def detach_resource_from_problem(problem_id: int, resource_id: int, conn: ConnectionDep):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM problem_resources
            WHERE problem_id = %s AND resource_id = %s
            """,
            (problem_id, resource_id),
        )
        link = cur.fetchone()

    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")

    with conn.cursor() as cur:
        cur.execute(
            """
            DELETE FROM problem_resources
            WHERE problem_id = %s AND resource_id = %s
            """,
            (problem_id, resource_id),
        )
    conn.commit()
    return build_problem_full(conn, problem_id)


@router.post("/solutions/{solution_id}/resources", response_model=schemas.SolutionRead)
def attach_resource_to_solution(solution_id: int, payload: schemas.SolutionResourceAttach, conn: ConnectionDep):
    get_solution_or_404(conn, solution_id)
    get_resource_or_404(conn, payload.resource_id)

    # Check if link exists
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM solution_resources
            WHERE solution_id = %s AND resource_id = %s
            """,
            (solution_id, payload.resource_id),
        )
        existing = cur.fetchone()

    if not existing:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO solution_resources (solution_id, resource_id)
                VALUES (%s, %s)
                """,
                (solution_id, payload.resource_id),
            )
        conn.commit()

    solution = get_solution_or_404(conn, solution_id)
    return schemas.SolutionRead.model_validate(solution)


@router.delete("/solutions/{solution_id}/resources/{resource_id}", response_model=schemas.SolutionRead)
def detach_resource_from_solution(solution_id: int, resource_id: int, conn: ConnectionDep):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM solution_resources
            WHERE solution_id = %s AND resource_id = %s
            """,
            (solution_id, resource_id),
        )
        link = cur.fetchone()

    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")

    with conn.cursor() as cur:
        cur.execute(
            """
            DELETE FROM solution_resources
            WHERE solution_id = %s AND resource_id = %s
            """,
            (solution_id, resource_id),
        )
    conn.commit()

    solution = get_solution_or_404(conn, solution_id)
    return schemas.SolutionRead.model_validate(solution)
