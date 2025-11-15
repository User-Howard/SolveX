import pandas as pd
from sqlalchemy import Engine
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TABLES_DIR = BASE_DIR / "tables"
def load_tables(engine: Engine):
    csv_path = TABLES_DIR / "problems.csv"
    df = pd.read_csv(csv_path)
    df.to_sql("problems", con=engine, if_exists="append", index=False)
