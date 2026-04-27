import pandas as pd
from sqlalchemy import create_engine
import os

DB_PATH = "sqlite:///../database/business.db"
# Absolute path hack for reliability when running from different dirs
current_dir = os.path.dirname(os.path.abspath(__file__))
db_abs_path = os.path.join(current_dir, '..', 'database', 'business.db')
ENGINE_URL = f"sqlite:///{db_abs_path}"

def execute_query(sql: str) -> pd.DataFrame:
    try:
        engine = create_engine(ENGINE_URL)
        df = pd.read_sql(sql, engine)
        return df
    except Exception as e:
        return pd.DataFrame({"error": [str(e)]})
