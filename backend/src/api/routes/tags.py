from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.api import schemas
from src.api.deps import SessionDep
from src.api.routes.utils import get_problem_or_404, get_resource_or_404, get_tag_or_404
from src.api.services.resources import build_resource_detail
from src.db import models


router = APIRouter(tags=["tags"])


@router.post("/tags", response_model=schemas.TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(payload: schemas.TagCreate, session: SessionDep):
    tag = models.Tag(
        tag_name=payload.tag_name,
        category=payload.category,
        description=payload.description,
    )
    session.add(tag)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag already exists") from exc
    session.refresh(tag)
    return tag


@router.get("/tags", response_model=list[schemas.TagRead])
def list_tags(session: SessionDep):
    stmt = select(models.Tag).order_by(models.Tag.tag_name)
    tags = session.execute(stmt).scalars().all()
    return tags


@router.post("/problems/{problem_id}/tags", response_model=schemas.ProblemWithAuthor)
def assign_tag_to_problem(problem_id: int, payload: schemas.ProblemTagAssign, session: SessionDep):
    problem = get_problem_or_404(session, problem_id)
    get_tag_or_404(session, payload.tag_id)
    stmt = (
        select(models.ProblemTag)
        .where(
            models.ProblemTag.problem_id == problem_id,
            models.ProblemTag.tag_id == payload.tag_id,
        )
    )
    existing = session.execute(stmt).scalar_one_or_none()
    if not existing:
        session.add(models.ProblemTag(problem_id=problem_id, tag_id=payload.tag_id))
        session.commit()
    session.refresh(problem)
    return get_problem_or_404(session, problem_id)


@router.delete("/problems/{problem_id}/tags/{tag_id}", response_model=schemas.ProblemWithAuthor)
def remove_problem_tag(problem_id: int, tag_id: int, session: SessionDep):
    problem = get_problem_or_404(session, problem_id)
    stmt = (
        select(models.ProblemTag)
        .where(models.ProblemTag.problem_id == problem_id, models.ProblemTag.tag_id == tag_id)
    )
    link = session.execute(stmt).scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag link not found")
    session.delete(link)
    session.commit()
    session.refresh(problem)
    return problem


@router.post("/resources/{resource_id}/tags", response_model=schemas.ResourceDetail)
def assign_tag_to_resource(resource_id: int, payload: schemas.ResourceTagAssign, session: SessionDep):
    get_resource_or_404(session, resource_id)
    get_tag_or_404(session, payload.tag_id)
    stmt = (
        select(models.ResourceTag)
        .where(models.ResourceTag.resource_id == resource_id, models.ResourceTag.tag_id == payload.tag_id)
    )
    link = session.execute(stmt).scalar_one_or_none()
    if not link:
        link = models.ResourceTag(
            resource_id=resource_id,
            tag_id=payload.tag_id,
            confidence=payload.confidence,
        )
        session.add(link)
    else:
        link.confidence = payload.confidence
    session.commit()
    return build_resource_detail(session, resource_id)


@router.delete("/resources/{resource_id}/tags/{tag_id}", response_model=schemas.ResourceDetail)
def remove_resource_tag(resource_id: int, tag_id: int, session: SessionDep):
    get_resource_or_404(session, resource_id)
    stmt = (
        select(models.ResourceTag)
        .where(models.ResourceTag.resource_id == resource_id, models.ResourceTag.tag_id == tag_id)
    )
    link = session.execute(stmt).scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag link not found")
    session.delete(link)
    session.commit()
    return build_resource_detail(session, resource_id)
