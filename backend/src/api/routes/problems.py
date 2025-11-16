from fastapi import APIRouter, status
from sqlalchemy import desc, func, select

from src.api import schemas
from src.api.deps import SessionDep
from src.api.routes.utils import (
    get_problem_or_404,
    get_problem_with_author,
    get_tag_or_404,
    get_user_or_404,
)
from src.api.services.problems import build_problem_full
from src.db import models


router = APIRouter(prefix="/problems", tags=["problems"])


@router.post("", response_model=schemas.ProblemRead, status_code=status.HTTP_201_CREATED)
def create_problem(payload: schemas.ProblemCreate, session: SessionDep):
    get_user_or_404(session, payload.user_id)
    problem = models.Problem(
        user_id=payload.user_id,
        title=payload.title,
        description=payload.description,
        problem_type=payload.problem_type,
    )
    session.add(problem)
    if payload.tags:
        unique_tags = set(payload.tags)
        for tag_id in unique_tags:
            get_tag_or_404(session, tag_id)
            problem.tags.append(models.ProblemTag(tag_id=tag_id))
    session.commit()
    session.refresh(problem)
    return problem


@router.get("/{problem_id}", response_model=schemas.ProblemWithAuthor)
def get_problem(problem_id: int, session: SessionDep):
    return get_problem_with_author(session, problem_id)


@router.patch("/{problem_id}", response_model=schemas.ProblemRead)
def update_problem(problem_id: int, payload: schemas.ProblemUpdate, session: SessionDep):
    problem = get_problem_or_404(session, problem_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(problem, field, value)
    session.commit()
    session.refresh(problem)
    return problem


@router.delete("/{problem_id}")
def delete_problem(problem_id: int, session: SessionDep):
    problem = get_problem_or_404(session, problem_id)
    session.delete(problem)
    session.commit()
    return {"deleted": True}


@router.get("", response_model=list[schemas.ProblemListItem])
def search_problems(
    session: SessionDep,
    keyword: str | None = None,
    type: str | None = None,
    tag: str | None = None,
):
    stmt = select(models.Problem)
    if keyword:
        like_pattern = f"%{keyword.lower()}%"
        stmt = stmt.where(
            func.lower(models.Problem.title).like(like_pattern)
            | func.lower(func.coalesce(models.Problem.description, "")).like(like_pattern)
        )
    if type:
        stmt = stmt.where(func.lower(models.Problem.problem_type) == type.lower())
    if tag:
        stmt = (
            stmt.join(models.ProblemTag)
            .join(models.Tag)
            .where(func.lower(models.Tag.tag_name) == tag.lower())
        )
    stmt = stmt.order_by(desc(models.Problem.created_at))
    problems = session.execute(stmt).scalars().unique().all()
    return problems


@router.post("/{problem_id}/resolve", response_model=schemas.ProblemRead)
def mark_problem_resolved(problem_id: int, session: SessionDep):
    problem = get_problem_or_404(session, problem_id)
    problem.resolved = True
    session.commit()
    session.refresh(problem)
    return problem


@router.get("/{problem_id}/full", response_model=schemas.ProblemFull)
def problem_full(problem_id: int, session: SessionDep):
    return build_problem_full(session, problem_id)
