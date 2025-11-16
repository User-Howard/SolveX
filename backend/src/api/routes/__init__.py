from fastapi import APIRouter

from . import dashboard, health, problems, relations, resources, solutions, tags, users

router = APIRouter()

router.include_router(health.router)
router.include_router(users.router)
router.include_router(problems.router)
router.include_router(solutions.router)
router.include_router(resources.router)
router.include_router(tags.router)
router.include_router(relations.router)
router.include_router(dashboard.router)

__all__ = ["router"]
