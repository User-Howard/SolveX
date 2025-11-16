from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from src.api import schemas
from src.api.routes.utils import get_resource_or_404
from src.db import models


def build_resource_detail(session: Session, resource_id: int) -> schemas.ResourceDetail:
    resource = get_resource_or_404(session, resource_id)

    problem_links_stmt = (
        select(models.Problem)
        .join(models.ProblemResource, models.Problem.problem_id == models.ProblemResource.problem_id)
        .where(models.ProblemResource.resource_id == resource_id)
        .order_by(desc(models.Problem.created_at))
    )
    linked_problems = session.execute(problem_links_stmt).scalars().all()

    solution_links_stmt = (
        select(models.Solution)
        .join(models.SolutionResource, models.Solution.solution_id == models.SolutionResource.solution_id)
        .where(models.SolutionResource.resource_id == resource_id)
        .order_by(desc(models.Solution.created_at))
    )
    linked_solutions = session.execute(solution_links_stmt).scalars().all()

    tags = [link.tag for link in resource.tags]

    return schemas.ResourceDetail(
        **schemas.ResourceRead.model_validate(resource).model_dump(),
        linked_problems=[
            schemas.ProblemListItem.model_validate(problem) for problem in linked_problems
        ],
        linked_solutions=[
            schemas.SolutionRead.model_validate(solution) for solution in linked_solutions
        ],
        tags=[schemas.TagRead.model_validate(tag) for tag in tags],
    )
