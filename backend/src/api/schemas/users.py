from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from .base import ORMModel


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserPublic(ORMModel):
    user_id: int
    username: str


class UserRead(UserBase, ORMModel):
    user_id: int
    created_at: datetime


__all__ = [
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserPublic",
    "UserRead",
]
