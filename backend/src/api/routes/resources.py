from datetime import datetime

from fastapi import APIRouter, status
from sqlalchemy import desc, func, select

from src.api import schemas
from src.api.deps import SessionDep
from src.api.routes.utils import get_resource_or_404, get_user_or_404
from src.api.services.resources import build_resource_detail
from src.db import models


router = APIRouter(prefix="/resources", tags=["resources"])


@router.post("", response_model=schemas.ResourceRead, status_code=status.HTTP_201_CREATED)
def create_resource(payload: schemas.ResourceCreate, session: SessionDep):
    get_user_or_404(session, payload.user_id)
    now = datetime.utcnow()
    resource = models.Resource(
        user_id=payload.user_id,
        url=payload.url,
        title=payload.title,
        source_platform=payload.source_platform,
        content_summary=payload.content_summary,
        usefulness_score=payload.usefulness_score,
        first_visited_at=now,
        last_visited_at=now,
    )
    session.add(resource)
    session.commit()
    session.refresh(resource)
    return resource


@router.get("/{resource_id}", response_model=schemas.ResourceDetail)
def get_resource(resource_id: int, session: SessionDep):
    return build_resource_detail(session, resource_id)


@router.patch("/{resource_id}", response_model=schemas.ResourceRead)
def update_resource(resource_id: int, payload: schemas.ResourceUpdate, session: SessionDep):
    resource = get_resource_or_404(session, resource_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(resource, field, value)
    session.commit()
    session.refresh(resource)
    return resource


@router.post("/{resource_id}/visit", response_model=schemas.ResourceRead)
def visit_resource(resource_id: int, session: SessionDep):
    resource = get_resource_or_404(session, resource_id)
    now = datetime.utcnow()
    if not resource.first_visited_at:
        resource.first_visited_at = now
    resource.last_visited_at = now
    session.commit()
    session.refresh(resource)
    return resource


@router.get("", response_model=list[schemas.ResourceSummary])
def search_resources(
    session: SessionDep,
    tag: str | None = None,
    min_score: float | None = None,
    keyword: str | None = None,
):
    stmt = select(models.Resource)
    if tag:
        stmt = stmt.join(models.ResourceTag).join(models.Tag).where(func.lower(models.Tag.tag_name) == tag.lower())
    if min_score is not None:
        stmt = stmt.where(models.Resource.usefulness_score >= min_score)
    if keyword:
        like_pattern = f"%{keyword.lower()}%"
        stmt = stmt.where(
            func.lower(models.Resource.title).like(like_pattern)
            | func.lower(func.coalesce(models.Resource.content_summary, "")).like(like_pattern)
        )
    stmt = stmt.order_by(desc(models.Resource.last_visited_at), desc(models.Resource.resource_id))
    resources = session.execute(stmt).scalars().unique().all()
    return resources
