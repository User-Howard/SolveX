from __future__ import annotations
from typing import List, Optional

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .session import Base


# ------------------------------------------------------
# User
# ------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(50))
    last_name: Mapped[Optional[str]] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    problems: Mapped[List["Problem"]] = relationship(
        back_populates="author", cascade="all, delete-orphan"
    )

    resources: Mapped[List["Resource"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )


# ------------------------------------------------------
# Problem
# ------------------------------------------------------
class Problem(Base):
    __tablename__ = "problems"

    problem_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    problem_type: Mapped[Optional[str]] = mapped_column(String(100))
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    resolved: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))

    author: Mapped["User"] = relationship(back_populates="problems")

    solutions: Mapped[List["Solution"]] = relationship(
        back_populates="problem", cascade="all, delete-orphan"
    )

    resources: Mapped[List["ProblemResource"]] = relationship(
        back_populates="problem", cascade="all, delete-orphan"
    )

    tags: Mapped[List["ProblemTag"]] = relationship(
        back_populates="problem", cascade="all, delete-orphan"
    )

    outward_relations: Mapped[List["ProblemRelation"]] = relationship(
        foreign_keys="ProblemRelation.from_problem_id",
        back_populates="from_problem",
        cascade="all, delete-orphan",
    )

    inward_relations: Mapped[List["ProblemRelation"]] = relationship(
        foreign_keys="ProblemRelation.to_problem_id",
        back_populates="to_problem",
        cascade="all, delete-orphan",
    )


# ------------------------------------------------------
# Solution
# ------------------------------------------------------
class Solution(Base):
    __tablename__ = "solutions"
    __table_args__ = (
        CheckConstraint("solution_id != parent_solution_id", name="no_self_loop"),
        CheckConstraint("success_rate >= 0 AND success_rate <= 100", name="solution_success_rate_range"),
    )

    solution_id: Mapped[int] = mapped_column(primary_key=True)
    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.problem_id"), nullable=False)
    parent_solution_id: Mapped[Optional[int]] = mapped_column(ForeignKey("solutions.solution_id"))

    code_snippet: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[Optional[str]] = mapped_column(Text)
    approach_type: Mapped[Optional[str]] = mapped_column(String(100))
    version_number: Mapped[int] = mapped_column(Integer, server_default="1")
    branch_type: Mapped[Optional[str]] = mapped_column(String(50))
    improvement_description: Mapped[Optional[str]] = mapped_column(Text)
    success_rate: Mapped[Optional[float]] = mapped_column(Float)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    problem: Mapped["Problem"] = relationship(back_populates="solutions")

    parent_solution: Mapped[Optional["Solution"]] = relationship(
        remote_side="Solution.solution_id", back_populates="children"
    )
    children: Mapped[List["Solution"]] = relationship(back_populates="parent_solution")

    resources: Mapped[List["SolutionResource"]] = relationship(
        back_populates="solution", cascade="all, delete-orphan"
    )


# ------------------------------------------------------
# Resource
# ------------------------------------------------------
class Resource(Base):
    __tablename__ = "resources"
    __table_args__ = (
        CheckConstraint("usefulness_score >= 0 AND usefulness_score <= 5", name="resource_usefulness_range"),
    )

    resource_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)

    url: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String(500))
    source_platform: Mapped[Optional[str]] = mapped_column(String(50))
    content_summary: Mapped[Optional[str]] = mapped_column(Text)
    visit_count: Mapped[int] = mapped_column(Integer, server_default="1")
    first_visited_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    last_visited_at: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    usefulness_score: Mapped[Optional[float]] = mapped_column(Float)

    owner: Mapped["User"] = relationship(back_populates="resources")

    problems: Mapped[List["ProblemResource"]] = relationship(
        back_populates="resource", cascade="all, delete-orphan"
    )
    solutions: Mapped[List["SolutionResource"]] = relationship(
        back_populates="resource", cascade="all, delete-orphan"
    )
    tags: Mapped[List["ResourceTag"]] = relationship(
        back_populates="resource", cascade="all, delete-orphan"
    )


# ------------------------------------------------------
# Tag
# ------------------------------------------------------
class Tag(Base):
    __tablename__ = "tags"

    tag_id: Mapped[int] = mapped_column(primary_key=True)
    tag_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(Text)

    problem_links: Mapped[List["ProblemTag"]] = relationship(back_populates="tag")
    resource_links: Mapped[List["ResourceTag"]] = relationship(back_populates="tag")


# ------------------------------------------------------
# Relationships
# ------------------------------------------------------
class ProblemResource(Base):
    __tablename__ = "problem_resources"
    __table_args__ = (
        CheckConstraint("relevance_score >= 0 AND relevance_score <= 1", name="problem_resource_relevance_range"),
    )

    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.problem_id"), primary_key=True)
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.resource_id"), primary_key=True)

    relevance_score: Mapped[Optional[float]] = mapped_column(Float)
    contribution_type: Mapped[Optional[str]] = mapped_column(String(50))
    added_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    problem: Mapped["Problem"] = relationship(back_populates="resources")
    resource: Mapped["Resource"] = relationship(back_populates="problems")


class SolutionResource(Base):
    __tablename__ = "solution_resources"

    solution_id: Mapped[int] = mapped_column(ForeignKey("solutions.solution_id"), primary_key=True)
    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.resource_id"), primary_key=True)

    solution: Mapped["Solution"] = relationship(back_populates="resources")
    resource: Mapped["Resource"] = relationship(back_populates="solutions")


class ProblemRelation(Base):
    __tablename__ = "problem_relations"
    __table_args__ = (
        CheckConstraint("strength >= 0 AND strength <= 1", name="problem_relation_strength_range"),
        CheckConstraint("from_problem_id != to_problem_id", name="no_self_relation"),
    )

    from_problem_id: Mapped[int] = mapped_column(ForeignKey("problems.problem_id"), primary_key=True)
    to_problem_id: Mapped[int] = mapped_column(ForeignKey("problems.problem_id"), primary_key=True)

    relation_type: Mapped[Optional[str]] = mapped_column(String(50))
    strength: Mapped[Optional[float]] = mapped_column(Float)

    from_problem: Mapped["Problem"] = relationship(
        foreign_keys=[from_problem_id], back_populates="outward_relations"
    )
    to_problem: Mapped["Problem"] = relationship(
        foreign_keys=[to_problem_id], back_populates="inward_relations"
    )


class ProblemTag(Base):
    __tablename__ = "problem_tags"

    problem_id: Mapped[int] = mapped_column(ForeignKey("problems.problem_id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.tag_id"), primary_key=True)

    problem: Mapped["Problem"] = relationship(back_populates="tags")
    tag: Mapped["Tag"] = relationship(back_populates="problem_links")


class ResourceTag(Base):
    __tablename__ = "resource_tags"
    __table_args__ = (
        CheckConstraint("confidence >= 0 AND confidence <= 1", name="resource_tag_confidence_range"),
    )

    resource_id: Mapped[int] = mapped_column(ForeignKey("resources.resource_id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.tag_id"), primary_key=True)

    confidence: Mapped[Optional[float]] = mapped_column(Float)

    resource: Mapped["Resource"] = relationship(back_populates="tags")
    tag: Mapped["Tag"] = relationship(back_populates="resource_links")
