from __future__ import annotations

from typing import Optional

from pydantic import BaseModel

from .base import ORMModel


class TagBase(BaseModel):
    tag_name: str
    category: Optional[str] = None
    description: Optional[str] = None


class TagCreate(TagBase):
    pass


class TagRead(TagBase, ORMModel):
    tag_id: int


__all__ = ["TagBase", "TagCreate", "TagRead"]
