from fastapi import APIRouter, status

from src.api import schemas
from src.api.deps import ConnectionDep
from src.api.routes.utils import get_problem_or_404, get_problem_with_author, get_tag_or_404, get_user_or_404
from src.api.services.problems import build_problem_full


router = APIRouter(prefix="/problems", tags=["problems"])


@router.post("", response_model=schemas.ProblemRead, status_code=status.HTTP_201_CREATED)
def create_problem(payload: schemas.ProblemCreate, conn: ConnectionDep):
    get_user_or_404(conn, payload.user_id)

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO problems (user_id, title, description, problem_type)
            VALUES (%s, %s, %s, %s)
            RETURNING *
            """,
            (payload.user_id, payload.title, payload.description, payload.problem_type),
        )
        row = cur.fetchone()

    problem_id = row["problem_id"]

    # Add tags if provided
    if payload.tags:
        unique_tags = set(payload.tags)
        for tag_id in unique_tags:
            get_tag_or_404(conn, tag_id)
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO problem_tags (problem_id, tag_id)
                    VALUES (%s, %s)
                    """,
                    (problem_id, tag_id),
                )

    conn.commit()
    return schemas.ProblemRead.model_validate(row)


@router.get("/{problem_id}", response_model=schemas.ProblemWithAuthor)
def get_problem(problem_id: int, conn: ConnectionDep):
    problem_data = get_problem_with_author(conn, problem_id)
    return schemas.ProblemWithAuthor.model_validate(problem_data)


@router.patch("/{problem_id}", response_model=schemas.ProblemRead)
def update_problem(problem_id: int, payload: schemas.ProblemUpdate, conn: ConnectionDep):
    get_problem_or_404(conn, problem_id)
    updates = payload.model_dump(exclude_unset=True)

    if not updates:
        problem = get_problem_or_404(conn, problem_id)
        return schemas.ProblemRead.model_validate(problem)

    # Build dynamic SET clause
    set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
    values = list(updates.values()) + [problem_id]

    with conn.cursor() as cur:
        cur.execute(
            f"UPDATE problems SET {set_clause} WHERE problem_id = %s RETURNING *",
            values,
        )
        row = cur.fetchone()
    conn.commit()
    return schemas.ProblemRead.model_validate(row)


@router.delete("/{problem_id}")
def delete_problem(problem_id: int, conn: ConnectionDep):
    get_problem_or_404(conn, problem_id)
    with conn.cursor() as cur:
        cur.execute("DELETE FROM problems WHERE problem_id = %s", (problem_id,))
    conn.commit()
    return {"deleted": True}


@router.get("", response_model=list[schemas.ProblemListItem])
def search_problems(
    conn: ConnectionDep,
    keyword: str | None = None,
    type: str | None = None,
    tag: str | None = None,
):
    query = "SELECT DISTINCT p.* FROM problems p"
    params = []
    conditions = []

    if tag:
        query += " JOIN problem_tags pt ON p.problem_id = pt.problem_id"
        query += " JOIN tags t ON pt.tag_id = t.tag_id"
        conditions.append("LOWER(t.tag_name) = %s")
        params.append(tag.lower())

    if keyword:
        conditions.append(
            "(LOWER(p.title) LIKE %s OR LOWER(COALESCE(p.description, '')) LIKE %s)"
        )
        pattern = f"%{keyword.lower()}%"
        params.extend([pattern, pattern])

    if type:
        conditions.append("LOWER(p.problem_type) = %s")
        params.append(type.lower())

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY p.created_at DESC"

    with conn.cursor() as cur:
        cur.execute(query, params)
        rows = cur.fetchall()

    return [schemas.ProblemListItem.model_validate(row) for row in rows]


@router.post("/{problem_id}/resolve", response_model=schemas.ProblemRead)
def mark_problem_resolved(problem_id: int, conn: ConnectionDep):
    get_problem_or_404(conn, problem_id)

    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE problems
            SET resolved = TRUE
            WHERE problem_id = %s
            RETURNING *
            """,
            (problem_id,),
        )
        row = cur.fetchone()
    conn.commit()
    return schemas.ProblemRead.model_validate(row)


@router.get("/{problem_id}/full", response_model=schemas.ProblemFull)
def problem_full(problem_id: int, conn: ConnectionDep):
    return build_problem_full(conn, problem_id)
