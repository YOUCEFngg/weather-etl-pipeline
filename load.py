import os
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

def load_data(records):
    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

    df.to_sql(
        "weather_raw",
        engine,
        if_exists="append",
        index=False
    )
    print(f"Loaded {len(df)} records into PostgreSQL")
