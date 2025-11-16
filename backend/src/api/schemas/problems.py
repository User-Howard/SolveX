from __future__ import annotations

from datetime import datetime
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel

from .base import ORMModel

if TYPE_CHECKING:
    from .relations import ProblemRelationRead, ProblemResourceSummary
    from .solutions import SolutionRead
    from .tags import TagRead
    from .users import UserPublic


class ProblemBase(BaseModel):
    title: str
    description: Optional[str] = None
    problem_type: Optional[str] = None


class ProblemCreate(ProblemBase):
    user_id: int
    tags: Optional[list[int]] = None


class ProblemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    problem_type: Optional[str] = None
    resolved: Optional[bool] = None


class ProblemRead(ProblemBase, ORMModel):
    problem_id: int
    user_id: int
    created_at: datetime
    resolved: bool


class ProblemWithAuthor(ProblemRead):
    author: "UserPublic"


class ProblemListItem(ORMModel):
    problem_id: int
    title: str
    resolved: bool
    created_at: datetime


class ProblemSearchResponse(ORMModel):
    results: list[ProblemListItem]


class ProblemFull(BaseModel):
    problem: ProblemWithAuthor
    solutions: list["SolutionRead"]
    tags: list["TagRead"]
    linked_resources: list["ProblemResourceSummary"]
    relations_out: list["ProblemRelationRead"]
    relations_in: list["ProblemRelationRead"]


__all__ = [
    "ProblemBase",
    "ProblemCreate",
    "ProblemUpdate",
    "ProblemRead",
    "ProblemWithAuthor",
    "ProblemListItem",
    "ProblemSearchResponse",
    "ProblemFull",
]
