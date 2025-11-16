from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from src.db import models


def get_user_or_404(session: Session, user_id: int) -> models.User:
    user = session.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def get_problem_or_404(session: Session, problem_id: int) -> models.Problem:
    problem = session.get(models.Problem, problem_id)
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")
    return problem


def get_problem_with_author(session: Session, problem_id: int) -> models.Problem:
    stmt = (
        select(models.Problem)
        .options(joinedload(models.Problem.author))
        .where(models.Problem.problem_id == problem_id)
    )
    problem = session.execute(stmt).scalar_one_or_none()
    if not problem:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problem not found")
    return problem


def get_solution_or_404(session: Session, solution_id: int) -> models.Solution:
    solution = session.get(models.Solution, solution_id)
    if not solution:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solution not found")
    return solution


def get_resource_or_404(session: Session, resource_id: int) -> models.Resource:
    resource = session.get(models.Resource, resource_id)
    if not resource:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return resource


def get_tag_or_404(session: Session, tag_id: int) -> models.Tag:
    tag = session.get(models.Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag
