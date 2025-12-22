from fastapi import APIRouter, HTTPException, status
from psycopg import errors

from src.api import schemas
from src.api.deps import ConnectionDep
from src.api.routes.utils import get_problem_or_404, get_problem_with_author, get_resource_or_404, get_tag_or_404


router = APIRouter(tags=["tags"])


@router.post("/tags", response_model=schemas.TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(payload: schemas.TagCreate, conn: ConnectionDep):
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO tags (tag_name, category, description)
                VALUES (%s, %s, %s)
                RETURNING *
                """,
                (payload.tag_name, payload.category, payload.description),
            )
            row = cur.fetchone()
        conn.commit()
        return schemas.TagRead.model_validate(row)
    except errors.UniqueViolation:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag already exists")


@router.get("/tags", response_model=list[schemas.TagRead])
def list_tags(conn: ConnectionDep):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tags ORDER BY tag_name")
        rows = cur.fetchall()
    return [schemas.TagRead.model_validate(row) for row in rows]


@router.post("/problems/{problem_id}/tags", response_model=schemas.ProblemWithAuthor)
def assign_tag_to_problem(problem_id: int, payload: schemas.ProblemTagAssign, conn: ConnectionDep):
    get_problem_or_404(conn, problem_id)
    get_tag_or_404(conn, payload.tag_id)

    # Check if link already exists
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM problem_tags
            WHERE problem_id = %s AND tag_id = %s
            """,
            (problem_id, payload.tag_id),
        )
        existing = cur.fetchone()

    if not existing:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO problem_tags (problem_id, tag_id)
                VALUES (%s, %s)
                """,
                (problem_id, payload.tag_id),
            )
        conn.commit()

    # Return problem with author
    problem_data = get_problem_with_author(conn, problem_id)
    return schemas.ProblemWithAuthor.model_validate(problem_data)


@router.delete("/problems/{problem_id}/tags/{tag_id}", response_model=schemas.ProblemWithAuthor)
def remove_problem_tag(problem_id: int, tag_id: int, conn: ConnectionDep):
    get_problem_or_404(conn, problem_id)

    # Check if link exists
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM problem_tags
            WHERE problem_id = %s AND tag_id = %s
            """,
            (problem_id, tag_id),
        )
        link = cur.fetchone()

    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag link not found")

    with conn.cursor() as cur:
        cur.execute(
            """
            DELETE FROM problem_tags
            WHERE problem_id = %s AND tag_id = %s
            """,
            (problem_id, tag_id),
        )
    conn.commit()

    # Return problem with author
    problem_data = get_problem_with_author(conn, problem_id)
    return schemas.ProblemWithAuthor.model_validate(problem_data)


@router.post("/resources/{resource_id}/tags", response_model=schemas.ResourceDetail)
def assign_tag_to_resource(resource_id: int, payload: schemas.ResourceTagAssign, conn: ConnectionDep):
    get_resource_or_404(conn, resource_id)
    get_tag_or_404(conn, payload.tag_id)

    # Check if link exists (upsert pattern)
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM resource_tags
            WHERE resource_id = %s AND tag_id = %s
            """,
            (resource_id, payload.tag_id),
        )
        existing = cur.fetchone()

    if not existing:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO resource_tags (resource_id, tag_id, confidence)
                VALUES (%s, %s, %s)
                """,
                (resource_id, payload.tag_id, payload.confidence),
            )
    else:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE resource_tags
                SET confidence = %s
                WHERE resource_id = %s AND tag_id = %s
                """,
                (payload.confidence, resource_id, payload.tag_id),
            )
    conn.commit()

    # Return ResourceDetail (will be properly implemented when services are migrated)
    # For now, return a simplified version
    from src.api.services.resources import build_resource_detail
    return build_resource_detail(conn, resource_id)


@router.delete("/resources/{resource_id}/tags/{tag_id}", response_model=schemas.ResourceDetail)
def remove_resource_tag(resource_id: int, tag_id: int, conn: ConnectionDep):
    get_resource_or_404(conn, resource_id)

    # Check if link exists
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM resource_tags
            WHERE resource_id = %s AND tag_id = %s
            """,
            (resource_id, tag_id),
        )
        link = cur.fetchone()

    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag link not found")

    with conn.cursor() as cur:
        cur.execute(
            """
            DELETE FROM resource_tags
            WHERE resource_id = %s AND tag_id = %s
            """,
            (resource_id, tag_id),
        )
    conn.commit()

    # Return ResourceDetail (will be properly implemented when services are migrated)
    from src.api.services.resources import build_resource_detail
    return build_resource_detail(conn, resource_id)
