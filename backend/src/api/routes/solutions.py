from fastapi import APIRouter, HTTPException, status

from src.api import schemas
from src.api.deps import ConnectionDep
from src.api.routes.utils import get_problem_or_404, get_solution_or_404


router = APIRouter(tags=["solutions"])


@router.post(
    "/problems/{problem_id}/solutions",
    response_model=schemas.SolutionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_solution(problem_id: int, payload: schemas.SolutionCreate, conn: ConnectionDep):
    if payload.problem_id != problem_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Problem ID mismatch")

    get_problem_or_404(conn, problem_id)

    if payload.parent_solution_id:
        get_solution_or_404(conn, payload.parent_solution_id)

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO solutions (
                problem_id, parent_solution_id, code_snippet, explanation,
                approach_type, improvement_description, success_rate, branch_type
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
            """,
            (
                problem_id,
                payload.parent_solution_id,
                payload.code_snippet,
                payload.explanation,
                payload.approach_type,
                payload.improvement_description,
                payload.success_rate,
                payload.branch_type,
            ),
        )
        row = cur.fetchone()
    conn.commit()
    return schemas.SolutionRead.model_validate(row)


@router.get("/solutions/{solution_id}", response_model=schemas.SolutionDetail)
def get_solution(solution_id: int, conn: ConnectionDep):
    solution = get_solution_or_404(conn, solution_id)

    # Get children count
    with conn.cursor() as cur:
        cur.execute(
            "SELECT COUNT(*) as count FROM solutions WHERE parent_solution_id = %s",
            (solution_id,),
        )
        children_count = cur.fetchone()["count"]

    # Get parent solution if exists
    parent = None
    if solution["parent_solution_id"]:
        parent = get_solution_or_404(conn, solution["parent_solution_id"])

    return schemas.SolutionDetail(
        **schemas.SolutionRead.model_validate(solution).model_dump(),
        children_count=children_count,
        parent_solution=schemas.SolutionRead.model_validate(parent) if parent else None,
    )


@router.patch("/solutions/{solution_id}", response_model=schemas.SolutionRead)
def update_solution(solution_id: int, payload: schemas.SolutionUpdate, conn: ConnectionDep):
    solution = get_solution_or_404(conn, solution_id)
    updates = payload.model_dump(exclude_unset=True)

    if not updates:
        return schemas.SolutionRead.model_validate(solution)

    # Validate references if being updated
    if "parent_solution_id" in updates and updates["parent_solution_id"]:
        get_solution_or_404(conn, updates["parent_solution_id"])

    if "problem_id" in updates and updates["problem_id"] and updates["problem_id"] != solution["problem_id"]:
        get_problem_or_404(conn, updates["problem_id"])

    # Build dynamic SET clause
    set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
    values = list(updates.values()) + [solution_id]

    with conn.cursor() as cur:
        cur.execute(
            f"UPDATE solutions SET {set_clause} WHERE solution_id = %s RETURNING *",
            values,
        )
        row = cur.fetchone()
    conn.commit()
    return schemas.SolutionRead.model_validate(row)


@router.delete("/solutions/{solution_id}")
def delete_solution(solution_id: int, conn: ConnectionDep):
    get_solution_or_404(conn, solution_id)
    with conn.cursor() as cur:
        cur.execute("DELETE FROM solutions WHERE solution_id = %s", (solution_id,))
    conn.commit()
    return {"deleted": True}


@router.get("/problems/{problem_id}/solutions", response_model=list[schemas.SolutionRead])
def list_problem_solutions(problem_id: int, conn: ConnectionDep):
    get_problem_or_404(conn, problem_id)

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM solutions
            WHERE problem_id = %s
            ORDER BY created_at DESC
            """,
            (problem_id,),
        )
        rows = cur.fetchall()

    return [schemas.SolutionRead.model_validate(row) for row in rows]


@router.get("/solutions/{solution_id}/children", response_model=list[schemas.SolutionRead])
def get_solution_children(solution_id: int, conn: ConnectionDep):
    get_solution_or_404(conn, solution_id)

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM solutions
            WHERE parent_solution_id = %s
            ORDER BY created_at DESC
            """,
            (solution_id,),
        )
        rows = cur.fetchall()

    return [schemas.SolutionRead.model_validate(row) for row in rows]
