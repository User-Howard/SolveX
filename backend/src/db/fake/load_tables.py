from pathlib import Path
from typing import Dict, List

import pandas as pd
import psycopg

from src.config import settings

BASE_DIR = Path(__file__).resolve().parent
TABLES_DIR = BASE_DIR / "tables"

TABLES: List[Dict[str, object]] = [
    {"name": "users", "file": "users.csv", "datetime": ["created_at"]},
    {
        "name": "problems",
        "file": "problems.csv",
        "datetime": ["created_at"],
        "bool": ["resolved"],
    },
    {"name": "solutions", "file": "solutions.csv", "datetime": ["created_at"]},
    {
        "name": "resources",
        "file": "resources.csv",
        "datetime": ["first_visited_at", "last_visited_at"],
    },
    {"name": "tags", "file": "tags.csv"},
    {"name": "problem_resources", "file": "problem_resources.csv", "datetime": ["added_at"]},
    {"name": "solution_resources", "file": "solution_resources.csv"},
    {"name": "problem_relations", "file": "problem_relations.csv"},
    {"name": "problem_tags", "file": "problem_tags.csv"},
    {"name": "resource_tags", "file": "resource_tags.csv"},
]


def _coerce_datetimes(df: pd.DataFrame, columns: List[str]):
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column])


def _coerce_bools(df: pd.DataFrame, columns: List[str]):
    truthy = {"true", "1", "t", "y", "yes"}
    falsy = {"false", "0", "f", "n", "no"}

    def _convert(value):
        if isinstance(value, bool) or pd.isna(value):
            return value

        normalized = str(value).strip().lower()
        if normalized in truthy:
            return True
        if normalized in falsy:
            return False
        return bool(value)

    for column in columns:
        if column in df.columns:
            df[column] = df[column].map(_convert)


def _reset_sequences(conn: psycopg.Connection):
    """Reset PostgreSQL sequences after loading data with explicit IDs."""
    tables_with_sequences = [
        ("users", "user_id"),
        ("problems", "problem_id"),
        ("solutions", "solution_id"),
        ("resources", "resource_id"),
        ("tags", "tag_id"),
    ]

    with conn.cursor() as cur:
        for table_name, id_column in tables_with_sequences:
            cur.execute(
                f"""
                SELECT setval(
                    pg_get_serial_sequence('{table_name}', '{id_column}'),
                    COALESCE((SELECT MAX({id_column}) FROM {table_name}), 1),
                    true
                )
                """
            )
    print("✓ PostgreSQL sequences reset successfully")


def load_tables():
    """Load CSV test data into the database."""
    with psycopg.connect(settings.database_url) as conn:
        for table in TABLES:
            csv_path = TABLES_DIR / table["file"]
            df = pd.read_csv(csv_path)

            # Convert data types
            _coerce_datetimes(df, table.get("datetime", []))
            _coerce_bools(df, table.get("bool", []))

            # Replace NaN with None for proper NULL handling
            df = df.where(pd.notna(df), None)

            # Convert float columns that should be integers
            for col in df.columns:
                if df[col].dtype == 'float64':
                    # Check if this column only has integer values or None
                    non_null = df[col].dropna()
                    if len(non_null) > 0 and all(non_null == non_null.astype(int)):
                        df[col] = df[col].astype('Int64')  # Nullable integer type

            # Convert to list of tuples for bulk insert
            # Replace pd.NA with None for proper NULL handling
            records = [
                tuple(None if pd.isna(val) else val for val in row)
                for row in df.values
            ]

            # Build INSERT statement
            placeholders = ",".join(["%s"] * len(df.columns))
            table_name = table["name"]

            with conn.cursor() as cur:
                cur.executemany(
                    f"INSERT INTO {table_name} VALUES ({placeholders})",
                    records,
                )

            print(f"✓ Loaded {len(records)} records into {table_name}")

        # Reset sequences after loading all data
        _reset_sequences(conn)
        conn.commit()
        print("✓ All data loaded successfully")
