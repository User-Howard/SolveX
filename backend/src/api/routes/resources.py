from datetime import datetime

from fastapi import APIRouter, status

from src.api import schemas
from src.api.deps import ConnectionDep
from src.api.routes.utils import get_resource_or_404, get_user_or_404
from src.api.services.resources import build_resource_detail


router = APIRouter(prefix="/resources", tags=["resources"])


@router.post("", response_model=schemas.ResourceRead, status_code=status.HTTP_201_CREATED)
def create_resource(payload: schemas.ResourceCreate, conn: ConnectionDep):
    get_user_or_404(conn, payload.user_id)
    now = datetime.now()

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO resources (
                user_id, url, title, source_platform, content_summary,
                usefulness_score, first_visited_at, last_visited_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
            """,
            (
                payload.user_id,
                payload.url,
                payload.title,
                payload.source_platform,
                payload.content_summary,
                payload.usefulness_score,
                now,
                now,
            ),
        )
        row = cur.fetchone()
    conn.commit()
    return schemas.ResourceRead.model_validate(row)


@router.get("/{resource_id}", response_model=schemas.ResourceDetail)
def get_resource(resource_id: int, conn: ConnectionDep):
    return build_resource_detail(conn, resource_id)


@router.patch("/{resource_id}", response_model=schemas.ResourceRead)
def update_resource(resource_id: int, payload: schemas.ResourceUpdate, conn: ConnectionDep):
    get_resource_or_404(conn, resource_id)
    updates = payload.model_dump(exclude_unset=True)

    if not updates:
        resource = get_resource_or_404(conn, resource_id)
        return schemas.ResourceRead.model_validate(resource)

    # Build dynamic SET clause
    set_clause = ", ".join([f"{k} = %s" for k in updates.keys()])
    values = list(updates.values()) + [resource_id]

    with conn.cursor() as cur:
        cur.execute(
            f"UPDATE resources SET {set_clause} WHERE resource_id = %s RETURNING *",
            values,
        )
        row = cur.fetchone()
    conn.commit()
    return schemas.ResourceRead.model_validate(row)


@router.post("/{resource_id}/visit", response_model=schemas.ResourceRead)
def visit_resource(resource_id: int, conn: ConnectionDep):
    get_resource_or_404(conn, resource_id)

    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE resources
            SET visit_count = visit_count + 1,
                last_visited_at = %s
            WHERE resource_id = %s
            RETURNING *
            """,
            (datetime.now(), resource_id),
        )
        row = cur.fetchone()
    conn.commit()
    return schemas.ResourceRead.model_validate(row)


@router.get("", response_model=list[schemas.ResourceSummary])
def search_resources(
    conn: ConnectionDep,
    tag: str | None = None,
    min_score: float | None = None,
    keyword: str | None = None,
):
    query = "SELECT DISTINCT r.* FROM resources r"
    params = []
    conditions = []

    if tag:
        query += " JOIN resource_tags rt ON r.resource_id = rt.resource_id"
        query += " JOIN tags t ON rt.tag_id = t.tag_id"
        conditions.append("LOWER(t.tag_name) = %s")
        params.append(tag.lower())

    if min_score is not None:
        conditions.append("r.usefulness_score >= %s")
        params.append(min_score)

    if keyword:
        conditions.append(
            "(LOWER(r.title) LIKE %s OR LOWER(COALESCE(r.content_summary, '')) LIKE %s)"
        )
        pattern = f"%{keyword.lower()}%"
        params.extend([pattern, pattern])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY r.last_visited_at DESC, r.resource_id DESC"

    with conn.cursor() as cur:
        cur.execute(query, params)
        rows = cur.fetchall()

    return [schemas.ResourceSummary.model_validate(row) for row in rows]
