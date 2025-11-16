from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel

from .base import ORMModel

if TYPE_CHECKING:
    from .problems import ProblemListItem
    from .solutions import SolutionRead


class TopTag(ORMModel):
    tag_id: int
    tag_name: str
    usage_count: int


class TopResource(ORMModel):
    resource_id: int
    title: str | None = None
    usage_count: int


class DashboardResponse(BaseModel):
    recent_problems: list["ProblemListItem"]
    recent_solutions: list["SolutionRead"]
    top_tags: list[TopTag]
    top_resources: list[TopResource]


__all__ = ["TopTag", "TopResource", "DashboardResponse"]
