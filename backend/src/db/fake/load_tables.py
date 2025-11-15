from pathlib import Path
from typing import Dict, List

import pandas as pd
from sqlalchemy import Engine

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


def load_tables(engine: Engine):
    for table in TABLES:
        csv_path = TABLES_DIR / table["file"]
        df = pd.read_csv(csv_path)

        _coerce_datetimes(df, table.get("datetime", []))
        _coerce_bools(df, table.get("bool", []))

        df.to_sql(table["name"], con=engine, if_exists="append", index=False)
