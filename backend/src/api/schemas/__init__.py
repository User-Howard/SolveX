from .base import ORMModel
from .users import UserBase, UserCreate, UserUpdate, UserPublic, UserRead
from .problems import (
    ProblemBase,
    ProblemCreate,
    ProblemUpdate,
    ProblemRead,
    ProblemWithAuthor,
    ProblemListItem,
    ProblemSearchResponse,
    ProblemFull,
)
from .solutions import (
    SolutionBase,
    SolutionCreate,
    SolutionUpdate,
    SolutionRead,
    SolutionDetail,
)
from .resources import (
    ResourceBase,
    ResourceCreate,
    ResourceUpdate,
    ResourceRead,
    ResourceSummary,
    ResourceDetail,
)
from .tags import TagBase, TagCreate, TagRead
from .relations import (
    ProblemTagAssign,
    ResourceTagAssign,
    ProblemResourceAttach,
    SolutionResourceAttach,
    ProblemRelationCreate,
    ProblemRelationRead,
    ProblemResourceSummary,
)
from .dashboard import TopTag, TopResource, DashboardResponse

__all__ = [
    "ORMModel",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserPublic",
    "UserRead",
    "ProblemBase",
    "ProblemCreate",
    "ProblemUpdate",
    "ProblemRead",
    "ProblemWithAuthor",
    "ProblemListItem",
    "ProblemSearchResponse",
    "ProblemFull",
    "SolutionBase",
    "SolutionCreate",
    "SolutionUpdate",
    "SolutionRead",
    "SolutionDetail",
    "ResourceBase",
    "ResourceCreate",
    "ResourceUpdate",
    "ResourceRead",
    "ResourceSummary",
    "ResourceDetail",
    "TagBase",
    "TagCreate",
    "TagRead",
    "ProblemTagAssign",
    "ResourceTagAssign",
    "ProblemResourceAttach",
    "SolutionResourceAttach",
    "ProblemRelationCreate",
    "ProblemRelationRead",
    "ProblemResourceSummary",
    "TopTag",
    "TopResource",
    "DashboardResponse",
]


ProblemWithAuthor.model_rebuild()
ProblemFull.model_rebuild()
SolutionDetail.model_rebuild()
ResourceDetail.model_rebuild()
ProblemResourceSummary.model_rebuild()
DashboardResponse.model_rebuild()
