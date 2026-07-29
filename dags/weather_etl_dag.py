from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

# Add app folder to Python path
sys.path.append('/opt/airflow/app')

from extract import get_weather
from bronze import save_to_bronze
from load import load_data

default_args = {
    'owner': 'you',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_weather_pipeline():
    cities = ["London", "Paris", "Algiers"]
    records = [get_weather(city) for city in cities]
    print(f"Extracted data for {len(records)} cities")
    save_to_bronze(records)
    load_data(records)
    print("Pipeline completed successfully!")

with DAG(
    'weather_etl_pipeline',
    default_args=default_args,
    description='Extract weather → Bronze (MinIO) → PostgreSQL',
    schedule='@hourly',
    start_date=datetime(2026, 7, 28),
    catchup=False,
    tags=['weather', 'etl', 'bronze'],
) as dag:

    run_pipeline = PythonOperator(
        task_id='run_weather_pipeline',
        python_callable=run_weather_pipeline,
    )
