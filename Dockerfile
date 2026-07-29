FROM python:3.11-slim

WORKDIR /app

# Install Java and other deps - using default-jre-headless (lighter, works everywhere)
RUN apt-get update --fix-missing && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    default-jre-headless \
    ca-certificates \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$JAVA_HOME/bin:$PATH

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-db.py .
COPY app/ .

CMD ["python", "main.py"]
