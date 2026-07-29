from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append('/opt/airflow/app')

from extract import get_weather
from bronze import save_to_bronze
from silver import bronze_to_silver
from load import load_data

default_args = {
    'owner': 'you',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract_task():
    cities = ["London", "Paris", "Algiers"]
    records = [get_weather(city) for city in cities]
    print(f"Extracted {len(records)} records")
    return records

def bronze_task(ti):
    records = ti.xcom_pull(task_ids='extract')
    save_to_bronze(records)
    print("Bronze layer saved to MinIO")

def silver_task(ti):
    records = ti.xcom_pull(task_ids='extract')
    bronze_to_silver(records)
    print("Silver layer created with Spark + Delta Lake")

def load_task():
    load_data()
    print("Data loaded from Silver to PostgreSQL")

with DAG(
    'weather_etl_pipeline',
    default_args=default_args,
    description='Extract → Bronze (MinIO) → Silver (Spark/Delta) → PostgreSQL',
    schedule='@hourly',
    start_date=datetime(2026, 7, 28),
    catchup=False,
    tags=['weather', 'etl', 'bronze', 'silver', 'spark', 'delta'],
) as dag:

    t1_extract = PythonOperator(
        task_id='extract',
        python_callable=extract_task,
    )

    t2_bronze = PythonOperator(
        task_id='bronze',
        python_callable=bronze_task,
    )

    t3_silver = PythonOperator(
        task_id='silver',
        python_callable=silver_task,
    )

    t4_load = PythonOperator(
        task_id='load',
        python_callable=load_task,
    )

    t1_extract >> t2_bronze >> t3_silver >> t4_load
