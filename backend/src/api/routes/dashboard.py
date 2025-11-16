from fastapi import APIRouter
from sqlalchemy import desc, func, select

from src.api import schemas
from src.api.deps import SessionDep
from src.api.routes.utils import get_user_or_404
from src.db import models


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/{user_id}", response_model=schemas.DashboardResponse)
def get_dashboard(user_id: int, session: SessionDep):
    get_user_or_404(session, user_id)
    recent_problems = session.execute(
        select(models.Problem)
        .where(models.Problem.user_id == user_id)
        .order_by(desc(models.Problem.created_at))
        .limit(10)
    ).scalars().all()

    recent_solutions = session.execute(
        select(models.Solution)
        .join(models.Problem)
        .where(models.Problem.user_id == user_id)
        .order_by(desc(models.Solution.created_at))
        .limit(10)
    ).scalars().all()

    tag_usage_stmt = (
        select(
            models.Tag.tag_id,
            models.Tag.tag_name,
            func.count(models.ProblemTag.problem_id).label("usage_count"),
        )
        .join(models.ProblemTag, models.Tag.tag_id == models.ProblemTag.tag_id, isouter=True)
        .group_by(models.Tag.tag_id)
        .order_by(desc("usage_count"))
        .limit(5)
    )
    tag_rows = session.execute(tag_usage_stmt).all()
    top_tags = [
        schemas.TopTag(tag_id=row.tag_id, tag_name=row.tag_name, usage_count=row.usage_count or 0)
        for row in tag_rows
    ]

    problem_links_subq = (
        select(func.count(models.ProblemResource.problem_id))
        .where(models.ProblemResource.resource_id == models.Resource.resource_id)
        .correlate(models.Resource)
        .scalar_subquery()
    )
    solution_links_subq = (
        select(func.count(models.SolutionResource.solution_id))
        .where(models.SolutionResource.resource_id == models.Resource.resource_id)
        .correlate(models.Resource)
        .scalar_subquery()
    )
    usage_expr = problem_links_subq + solution_links_subq
    top_resources_stmt = (
        select(
            models.Resource.resource_id,
            models.Resource.title,
            usage_expr.label("usage_count"),
        )
        .order_by(desc("usage_count"))
        .limit(5)
    )
    resource_rows = session.execute(top_resources_stmt).all()
    top_resources = [
        schemas.TopResource(
            resource_id=row.resource_id,
            title=row.title,
            usage_count=row.usage_count or 0,
        )
        for row in resource_rows
    ]

    return schemas.DashboardResponse(
        recent_problems=[
            schemas.ProblemListItem.model_validate(problem) for problem in recent_problems
        ],
        recent_solutions=[
            schemas.SolutionRead.model_validate(solution) for solution in recent_solutions
        ],
        top_tags=top_tags,
        top_resources=top_resources,
    )
