FROM apache/airflow:2.9.0

USER root
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    default-jre-headless \
    curl \
    ca-certificates \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$JAVA_HOME/bin:$PATH

USER airflow
RUN pip install --no-cache-dir \
    requests \
    pandas \
    sqlalchemy \
    psycopg2-binary \
    minio \
    pyspark==3.5.0 \
    delta-spark==3.2.0 \
    dbt-core \
    dbt-postgres
