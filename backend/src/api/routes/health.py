from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/")
def root():
    return {"message": "Hello"}


@router.get("/health")
def health_check():
    return {"status": "ok"}
