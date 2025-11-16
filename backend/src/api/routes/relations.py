from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.api import schemas
from src.api.deps import SessionDep
from src.api.routes.utils import (
    get_problem_or_404,
    get_resource_or_404,
    get_solution_or_404,
)
from src.api.services.problems import build_problem_full
from src.db import models


router = APIRouter(tags=["relations"])


@router.post("/problems/{problem_id}/relations", response_model=schemas.ProblemRelationRead, status_code=status.HTTP_201_CREATED)
def create_problem_relation(problem_id: int, payload: schemas.ProblemRelationCreate, session: SessionDep):
    get_problem_or_404(session, problem_id)
    get_problem_or_404(session, payload.to_problem_id)
    relation = models.ProblemRelation(
        from_problem_id=problem_id,
        to_problem_id=payload.to_problem_id,
        relation_type=payload.relation_type,
        strength=payload.strength,
    )
    session.add(relation)
    try:
        session.commit()
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Relation already exists") from exc
    return relation


@router.delete("/problems/{problem_id}/relations/{to_problem_id}")
def delete_problem_relation(problem_id: int, to_problem_id: int, session: SessionDep):
    stmt = (
        select(models.ProblemRelation)
        .where(
            models.ProblemRelation.from_problem_id == problem_id,
            models.ProblemRelation.to_problem_id == to_problem_id,
        )
    )
    relation = session.execute(stmt).scalar_one_or_none()
    if not relation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relation not found")
    session.delete(relation)
    session.commit()
    return {"deleted": True}


@router.get("/problems/{problem_id}/relations/out", response_model=list[schemas.ProblemRelationRead])
def list_problem_relations_out(problem_id: int, session: SessionDep):
    get_problem_or_404(session, problem_id)
    stmt = select(models.ProblemRelation).where(models.ProblemRelation.from_problem_id == problem_id)
    relations = session.execute(stmt).scalars().all()
    return relations


@router.get("/problems/{problem_id}/relations/in", response_model=list[schemas.ProblemRelationRead])
def list_problem_relations_in(problem_id: int, session: SessionDep):
    get_problem_or_404(session, problem_id)
    stmt = select(models.ProblemRelation).where(models.ProblemRelation.to_problem_id == problem_id)
    relations = session.execute(stmt).scalars().all()
    return relations


@router.post("/problems/{problem_id}/resources", response_model=schemas.ProblemFull)
def attach_resource_to_problem(problem_id: int, payload: schemas.ProblemResourceAttach, session: SessionDep):
    get_problem_or_404(session, problem_id)
    get_resource_or_404(session, payload.resource_id)
    stmt = (
        select(models.ProblemResource)
        .where(
            models.ProblemResource.problem_id == problem_id,
            models.ProblemResource.resource_id == payload.resource_id,
        )
    )
    link = session.execute(stmt).scalar_one_or_none()
    if not link:
        link = models.ProblemResource(
            problem_id=problem_id,
            resource_id=payload.resource_id,
            relevance_score=payload.relevance_score,
            contribution_type=payload.contribution_type,
        )
        session.add(link)
    else:
        link.relevance_score = payload.relevance_score
        link.contribution_type = payload.contribution_type
    session.commit()
    return build_problem_full(session, problem_id)


@router.delete("/problems/{problem_id}/resources/{resource_id}", response_model=schemas.ProblemFull)
def detach_resource_from_problem(problem_id: int, resource_id: int, session: SessionDep):
    stmt = (
        select(models.ProblemResource)
        .where(
            models.ProblemResource.problem_id == problem_id,
            models.ProblemResource.resource_id == resource_id,
        )
    )
    link = session.execute(stmt).scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
    session.delete(link)
    session.commit()
    return build_problem_full(session, problem_id)


@router.post("/solutions/{solution_id}/resources", response_model=schemas.SolutionRead)
def attach_resource_to_solution(solution_id: int, payload: schemas.SolutionResourceAttach, session: SessionDep):
    get_solution_or_404(session, solution_id)
    get_resource_or_404(session, payload.resource_id)
    stmt = (
        select(models.SolutionResource)
        .where(
            models.SolutionResource.solution_id == solution_id,
            models.SolutionResource.resource_id == payload.resource_id,
        )
    )
    link = session.execute(stmt).scalar_one_or_none()
    if not link:
        link = models.SolutionResource(solution_id=solution_id, resource_id=payload.resource_id)
        session.add(link)
        session.commit()
    return get_solution_or_404(session, solution_id)


@router.delete("/solutions/{solution_id}/resources/{resource_id}", response_model=schemas.SolutionRead)
def detach_resource_from_solution(solution_id: int, resource_id: int, session: SessionDep):
    stmt = (
        select(models.SolutionResource)
        .where(
            models.SolutionResource.solution_id == solution_id,
            models.SolutionResource.resource_id == resource_id,
        )
    )
    link = session.execute(stmt).scalar_one_or_none()
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attachment not found")
    session.delete(link)
    session.commit()
    return get_solution_or_404(session, solution_id)
