from fastapi import APIRouter, HTTPException, status
from psycopg import errors

from src.api import schemas
from src.api.deps import ConnectionDep
from src.api.routes.utils import get_user_or_404


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: schemas.UserCreate, conn: ConnectionDep):
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (username, email, first_name, last_name)
                VALUES (%s, %s, %s, %s)
                RETURNING *
                """,
                (payload.username, payload.email, payload.first_name, payload.last_name),
            )
            row = cur.fetchone()
        conn.commit()
        return schemas.UserRead.model_validate(row)
    except errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )


@router.get("/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, conn: ConnectionDep):
    user = get_user_or_404(conn, user_id)
    return schemas.UserRead.model_validate(user)


@router.patch("/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, payload: schemas.UserUpdate, conn: ConnectionDep):
    get_user_or_404(conn, user_id)
    updates = payload.model_dump(exclude_unset=True)

    if not updates:
        # No fields to update, return existing user
        user = get_user_or_404(conn, user_id)
        return schemas.UserRead.model_validate(user)

    # Build dynamic SET clause
    set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
    values = list(updates.values()) + [user_id]

    try:
        with conn.cursor() as cur:
            cur.execute(
                f"UPDATE users SET {set_clause} WHERE user_id = %s RETURNING *",
                values,
            )
            row = cur.fetchone()
        conn.commit()
        return schemas.UserRead.model_validate(row)
    except errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )


@router.get("/{user_id}/problems", response_model=list[schemas.ProblemListItem])
def list_user_problems(user_id: int, conn: ConnectionDep):
    get_user_or_404(conn, user_id)

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM problems
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,),
        )
        rows = cur.fetchall()

    return [schemas.ProblemListItem.model_validate(row) for row in rows]


@router.get("/{user_id}/resources", response_model=list[schemas.ResourceSummary])
def list_user_resources(user_id: int, conn: ConnectionDep):
    get_user_or_404(conn, user_id)

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM resources
            WHERE user_id = %s
            ORDER BY last_visited_at DESC, resource_id DESC
            """,
            (user_id,),
        )
        rows = cur.fetchall()

    return [schemas.ResourceSummary.model_validate(row) for row in rows]
