from fastapi import APIRouter, HTTPException, status
from sqlalchemy import desc, func, select

from src.api import schemas
from src.api.deps import SessionDep
from src.api.routes.utils import get_problem_or_404, get_solution_or_404
from src.db import models


router = APIRouter(tags=["solutions"])


@router.post(
    "/problems/{problem_id}/solutions",
    response_model=schemas.SolutionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_solution(problem_id: int, payload: schemas.SolutionCreate, session: SessionDep):
    if payload.problem_id != problem_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Problem ID mismatch")
    get_problem_or_404(session, problem_id)
    if payload.parent_solution_id:
        get_solution_or_404(session, payload.parent_solution_id)
    solution = models.Solution(
        problem_id=problem_id,
        parent_solution_id=payload.parent_solution_id,
        code_snippet=payload.code_snippet,
        explanation=payload.explanation,
        approach_type=payload.approach_type,
        improvement_description=payload.improvement_description,
        success_rate=payload.success_rate,
        branch_type=payload.branch_type,
    )
    session.add(solution)
    session.commit()
    session.refresh(solution)
    return solution


@router.get("/solutions/{solution_id}", response_model=schemas.SolutionDetail)
def get_solution(solution_id: int, session: SessionDep):
    solution = get_solution_or_404(session, solution_id)
    parent = solution.parent_solution
    children_count = session.scalar(
        select(func.count()).where(models.Solution.parent_solution_id == solution_id)
    )
    return schemas.SolutionDetail(
        **schemas.SolutionRead.model_validate(solution).model_dump(),
        children_count=children_count or 0,
        parent_solution=schemas.SolutionRead.model_validate(parent) if parent else None,
    )


@router.patch("/solutions/{solution_id}", response_model=schemas.SolutionRead)
def update_solution(solution_id: int, payload: schemas.SolutionUpdate, session: SessionDep):
    solution = get_solution_or_404(session, solution_id)
    data = payload.model_dump(exclude_unset=True)
    if "parent_solution_id" in data and data["parent_solution_id"]:
        get_solution_or_404(session, data["parent_solution_id"])
    if "problem_id" in data and data["problem_id"] and data["problem_id"] != solution.problem_id:
        get_problem_or_404(session, data["problem_id"])
    for field, value in data.items():
        setattr(solution, field, value)
    session.commit()
    session.refresh(solution)
    return solution


@router.delete("/solutions/{solution_id}")
def delete_solution(solution_id: int, session: SessionDep):
    solution = get_solution_or_404(session, solution_id)
    session.delete(solution)
    session.commit()
    return {"deleted": True}


@router.get("/problems/{problem_id}/solutions", response_model=list[schemas.SolutionRead])
def list_problem_solutions(problem_id: int, session: SessionDep):
    get_problem_or_404(session, problem_id)
    stmt = (
        select(models.Solution)
        .where(models.Solution.problem_id == problem_id)
        .order_by(desc(models.Solution.created_at))
    )
    solutions = session.execute(stmt).scalars().all()
    return solutions


@router.get("/solutions/{solution_id}/children", response_model=list[schemas.SolutionRead])
def get_solution_children(solution_id: int, session: SessionDep):
    get_solution_or_404(session, solution_id)
    stmt = (
        select(models.Solution)
        .where(models.Solution.parent_solution_id == solution_id)
        .order_by(desc(models.Solution.created_at))
    )
    children = session.execute(stmt).scalars().all()
    return children
