from __future__ import annotations

from datetime import datetime
from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, Field

from .base import ORMModel

if TYPE_CHECKING:
    from .problems import ProblemListItem
    from .solutions import SolutionRead
    from .tags import TagRead


class ResourceBase(BaseModel):
    url: str
    title: Optional[str] = None
    source_platform: Optional[str] = None
    content_summary: Optional[str] = None
    usefulness_score: Optional[float] = Field(default=None, ge=0, le=5)


class ResourceCreate(ResourceBase):
    user_id: int


class ResourceUpdate(BaseModel):
    title: Optional[str] = None
    content_summary: Optional[str] = None
    usefulness_score: Optional[float] = Field(default=None, ge=0, le=5)


class ResourceRead(ResourceBase, ORMModel):
    resource_id: int
    user_id: int
    first_visited_at: Optional[datetime] = None
    last_visited_at: Optional[datetime] = None


class ResourceSummary(ResourceRead):
    pass


class ResourceDetail(ResourceRead):
    linked_problems: list["ProblemListItem"]
    linked_solutions: list["SolutionRead"]
    tags: list["TagRead"]


__all__ = [
    "ResourceBase",
    "ResourceCreate",
    "ResourceUpdate",
    "ResourceRead",
    "ResourceSummary",
    "ResourceDetail",
]
