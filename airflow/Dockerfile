FROM apache/airflow:2.9.0

USER root
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

USER airflow
RUN pip install --no-cache-dir requests pandas sqlalchemy psycopg2-binary minio
