from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, Field

from .base import ORMModel


class ProblemTagAssign(BaseModel):
    tag_id: int


class ResourceTagAssign(BaseModel):
    tag_id: int
    confidence: Optional[float] = Field(default=None, ge=0, le=1)


class ProblemResourceAttach(BaseModel):
    resource_id: int
    relevance_score: Optional[float] = Field(default=None, ge=0, le=1)
    contribution_type: Optional[str] = None


class SolutionResourceAttach(BaseModel):
    resource_id: int


class ProblemRelationCreate(BaseModel):
    to_problem_id: int
    relation_type: Optional[str] = None
    strength: Optional[float] = Field(default=None, ge=0, le=1)


class ProblemRelationRead(ORMModel):
    from_problem_id: int
    to_problem_id: int
    relation_type: Optional[str] = None
    strength: Optional[float] = None


if TYPE_CHECKING:
    from .resources import ResourceRead


class ProblemResourceSummary(ORMModel):
    resource: "ResourceRead"
    relevance_score: Optional[float] = None
    contribution_type: Optional[str] = None


__all__ = [
    "ProblemTagAssign",
    "ResourceTagAssign",
    "ProblemResourceAttach",
    "SolutionResourceAttach",
    "ProblemRelationCreate",
    "ProblemRelationRead",
    "ProblemResourceSummary",
]
