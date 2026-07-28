FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy wait-for-db from root
COPY wait-for-db.py .

# Copy your app files from app/ folder into /app/ in container
COPY app/ .

CMD ["python", "main.py"]
