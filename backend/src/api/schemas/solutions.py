from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from .base import ORMModel


class SolutionBase(BaseModel):
    code_snippet: str
    explanation: Optional[str] = None
    approach_type: Optional[str] = None
    parent_solution_id: Optional[int] = None
    improvement_description: Optional[str] = None
    success_rate: Optional[float] = Field(default=None, ge=0, le=100)
    branch_type: Optional[str] = None


class SolutionCreate(SolutionBase):
    problem_id: int


class SolutionUpdate(BaseModel):
    code_snippet: Optional[str] = None
    explanation: Optional[str] = None
    approach_type: Optional[str] = None
    parent_solution_id: Optional[int] = None
    improvement_description: Optional[str] = None
    success_rate: Optional[float] = Field(default=None, ge=0, le=100)
    branch_type: Optional[str] = None
    version_number: Optional[int] = Field(default=None, ge=1)
    problem_id: Optional[int] = None


class SolutionRead(SolutionBase, ORMModel):
    solution_id: int
    problem_id: int
    version_number: int
    created_at: datetime


class SolutionDetail(SolutionRead):
    children_count: int
    parent_solution: Optional["SolutionRead"] = None


__all__ = [
    "SolutionBase",
    "SolutionCreate",
    "SolutionUpdate",
    "SolutionRead",
    "SolutionDetail",
]
