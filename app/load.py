import os
import pandas as pd
from sqlalchemy import create_engine
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip


def get_spark_session(app_name="WeatherLoad"):
    builder = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
    )
    spark = configure_spark_with_delta_pip(builder).getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    return spark


engine = create_engine(
    f"postgresql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)


def load_data():
    """
    Read from Silver Delta Lake and load into PostgreSQL.
    """
    print("\nReading from Silver Delta Lake...")
    
    spark = get_spark_session()
    silver_path = "/app/data/silver/weather"
    
    # Read Silver Delta table
    df_spark = spark.read.format("delta").load(silver_path)
    print(f"   Read {df_spark.count()} records from Silver")
    
    # Convert to Pandas for SQL loading
    df = df_spark.toPandas()
    
    # Load to PostgreSQL
    df.to_sql(
        "weather_silver",
        engine,
        if_exists="append",
        index=False
    )
    
    print(f"   Loaded {len(df)} records into PostgreSQL (weather_silver)")
    spark.stop()
