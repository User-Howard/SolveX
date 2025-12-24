from psycopg import errors
from fastapi import HTTPException, status


def handle_db_error(e: Exception):
    """Convert psycopg errors to HTTP exceptions."""
    if isinstance(e, errors.UniqueViolation):
        # Unique constraint violation (e.g., duplicate email, tag name)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resource already exists"
        )
    elif isinstance(e, errors.ForeignKeyViolation):
        # Referenced entity doesn't exist
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Referenced resource not found"
        )
    elif isinstance(e, errors.CheckViolation):
        # Check constraint failed (e.g., score out of range)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data validation failed"
        )
    elif isinstance(e, errors.NotNullViolation):
        # Required field is missing
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Required field is missing"
        )
    else:
        # Unknown database error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )
