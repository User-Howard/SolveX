import psycopg
from pathlib import Path

from src.config import settings


def init_db():
    """Initialize database: Create all tables from schema.sql."""
    schema_path = Path(__file__).parent / "schema.sql"

    with psycopg.connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(schema_path.read_text())
        conn.commit()
        print("Database schema created successfully.")


if __name__ == "__main__":
    init_db()