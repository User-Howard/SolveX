from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from psycopg import Connection

from src.db.connection import get_connection


def get_db() -> Generator[Connection, None, None]:
    with get_connection() as conn:
        yield conn


ConnectionDep = Annotated[Connection, Depends(get_db)]
