from contextlib import contextmanager

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from src.config import settings

# Create connection pool
pool = ConnectionPool(
    conninfo=settings.database_url,
    min_size=2,
    max_size=10,
    kwargs={"row_factory": dict_row},
)


@contextmanager
def get_connection():
    """Get a database connection from the pool."""
    with pool.connection() as conn:
        yield conn
