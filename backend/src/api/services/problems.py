from __future__ import annotations

from sqlalchemy import desc, select
from sqlalchemy.orm import Session, joinedload

from src.api import schemas
from src.api.routes.utils import get_problem_with_author
from src.db import models


def build_problem_full(session: Session, problem_id: int) -> schemas.ProblemFull:
    problem = get_problem_with_author(session, problem_id)
    solutions = session.execute(
        select(models.Solution)
        .where(models.Solution.problem_id == problem_id)
        .order_by(desc(models.Solution.created_at))
    ).scalars().all()

    tags = [link.tag for link in problem.tags]

    resource_links = session.execute(
        select(models.ProblemResource)
        .options(joinedload(models.ProblemResource.resource))
        .where(models.ProblemResource.problem_id == problem_id)
    ).scalars().all()

    relations_out = session.execute(
        select(models.ProblemRelation).where(models.ProblemRelation.from_problem_id == problem_id)
    ).scalars().all()
    relations_in = session.execute(
        select(models.ProblemRelation).where(models.ProblemRelation.to_problem_id == problem_id)
    ).scalars().all()

    return schemas.ProblemFull(
        problem=schemas.ProblemWithAuthor.model_validate(problem),
        solutions=[schemas.SolutionRead.model_validate(solution) for solution in solutions],
        tags=[schemas.TagRead.model_validate(tag) for tag in tags],
        linked_resources=[
            schemas.ProblemResourceSummary(
                resource=schemas.ResourceRead.model_validate(link.resource),
                relevance_score=link.relevance_score,
                contribution_type=link.contribution_type,
            )
            for link in resource_links
        ],
        relations_out=[schemas.ProblemRelationRead.model_validate(rel) for rel in relations_out],
        relations_in=[schemas.ProblemRelationRead.model_validate(rel) for rel in relations_in],
    )
