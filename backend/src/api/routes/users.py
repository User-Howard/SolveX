from fastapi import APIRouter, HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.exc import IntegrityError

from src.api import schemas
from src.api.deps import SessionDep
from src.api.routes.utils import get_user_or_404
from src.db import models


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: schemas.UserCreate, session: SessionDep):
    user = models.User(
        username=payload.username,
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
    )
    session.add(user)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        ) from exc
    session.refresh(user)
    return user


@router.get("/{user_id}", response_model=schemas.UserRead)
def get_user(user_id: int, session: SessionDep):
    return get_user_or_404(session, user_id)


@router.patch("/{user_id}", response_model=schemas.UserRead)
def update_user(user_id: int, payload: schemas.UserUpdate, session: SessionDep):
    user = get_user_or_404(session, user_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        ) from exc
    session.refresh(user)
    return user


@router.get("/{user_id}/problems", response_model=list[schemas.ProblemListItem])
def list_user_problems(user_id: int, session: SessionDep):
    get_user_or_404(session, user_id)
    stmt = (
        select(models.Problem)
        .where(models.Problem.user_id == user_id)
        .order_by(desc(models.Problem.created_at))
    )
    problems = session.execute(stmt).scalars().all()
    return problems


@router.get("/{user_id}/resources", response_model=list[schemas.ResourceSummary])
def list_user_resources(user_id: int, session: SessionDep):
    get_user_or_404(session, user_id)
    stmt = (
        select(models.Resource)
        .where(models.Resource.user_id == user_id)
        .order_by(desc(models.Resource.last_visited_at), desc(models.Resource.resource_id))
    )
    resources = session.execute(stmt).scalars().all()
    return resources
