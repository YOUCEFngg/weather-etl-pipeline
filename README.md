# 🌦️ Weather ETL Pipeline

> A production-grade data engineering project built with **Apache Airflow**, **Apache Spark**, **Delta Lake**, **dbt**, **MinIO**, **PostgreSQL**, and **Power BI** — all running in **Docker**.

---

## 📌 Project Overview

This project demonstrates a complete **Medallion Architecture** data pipeline that:

1. **Extracts** real-time weather data from the OpenWeatherMap API for 3 cities
2. **Stores** raw JSON responses in a Bronze layer (MinIO — S3-compatible data lake)
3. **Transforms** raw data into clean Silver tables using **PySpark + Delta Lake** (with ACID transactions, schema enforcement, and time travel)
4. **Models** business-ready Gold tables using **dbt** (SQL transformations)
5. **Loads** everything into **PostgreSQL** as a data warehouse
6. **Visualizes** insights in **Power BI**
7. **Orchestrates** the entire pipeline with **Apache Airflow** running on an hourly schedule

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           WEATHER ETL PIPELINE                               │
│                                                                              │
│   ┌──────────────┐                                                          │
│   │ OpenWeather  │                                                          │
│   │     API      │                                                          │
│   └──────┬───────┘                                                          │
│          │                                                                    │
│          ▼                                                                    │
│   ┌────────────────────────────────────────────────────────────────────┐     │
│   │                     APACHE AIRFLOW (Scheduler)                      │     │
│   │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌────┐│     │
│   │  │ extract │──▶│ bronze  │──▶│ silver  │──▶│  load   │──▶│dbt ││     │
│   │  │ (API)   │   │ (MinIO) │   │(Spark+  │   │(Postgre │   │(SQL││     │
│   │  │         │   │         │   │ Delta)  │   │  SQL)   │   │)   ││     │
│   │  └─────────┘   └─────────┘   └─────────┘   └─────────┘   └────┘│     │
│   │       │             │              │              │            │   │     │
│   └───────┼─────────────┼──────────────┼──────────────┼────────┼───┘     │
│           │             │              │              │            │         │
│           ▼             ▼              ▼              ▼            ▼         │
│   ┌──────────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐│
│   │  BRONZE      │  │  SILVER  │  │ PostgreSQL│  │   GOLD   │  │ Power BI ││
│   │  (MinIO)     │  │(Delta Lake│  │ weather_ │  │  (dbt)   │  │ Dashboard││
│   │              │  │          │  │  silver  │  │          │  │          ││
│   │ Raw JSON     │  │ Cleaned  │  │          │  │ gold_    │  │ Charts & ││
│   │ Timestamped  │  │ Typed    │  │          │  │ daily_   │  │  KPIs    ││
│   │ Untouched    │  │ Enriched │  │          │  │ weather  │  │          ││
│   │              │  │ ACID     │  │          │  │ gold_    │  │          ││
│   │              │  │ History  │  │          │  │ summary  │  │          ││
│   └──────────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘│
│                                                                              │
│   All services run inside Docker containers                                  │
│   Orchestrated by docker-compose up -d                                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Orchestration** | Apache Airflow | Schedules and monitors the entire pipeline hourly |
| **Data Lake (Bronze)** | MinIO | S3-compatible storage for raw JSON files |
| **Processing (Silver)** | Apache Spark + Delta Lake | Distributed data cleaning, type casting, enrichment |
| **Transformation (Gold)** | dbt (Data Build Tool) | SQL-based business logic and data modeling |
| **Data Warehouse** | PostgreSQL | Stores Silver and Gold tables for analytics |
| **Visualization** | Power BI | Dashboards and business reports |
| **Containerization** | Docker + Docker Compose | Reproducible, isolated environment |
| **Language** | Python 3.11 | ETL scripts and Spark jobs |

---

## 📊 Medallion Architecture

### 🥉 Bronze Layer — Raw Data
- **Location:** MinIO (`bronze/weather/raw_*.json`)
- **Content:** Raw API responses, untouched, timestamped
- **Why:** Preserve originals for recovery and reprocessing

### 🥈 Silver Layer — Clean Data
- **Location:** Delta Lake (`data/silver/weather/`)
- **Content:** Proper data types, derived columns (`temp_category`, `humidity_level`), metadata
- **Features:** ACID transactions, schema enforcement, time travel (`DESCRIBE HISTORY`)

### 🥇 Gold Layer — Business Tables
- **Location:** PostgreSQL (`gold.gold_daily_weather`, `gold.gold_weather_summary`)
- **Content:** Aggregations, KPIs, trends — ready for dashboards
- **Built with:** dbt SQL models

---

## 🚀 Quick Start

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- [WSL2](https://docs.microsoft.com/en-us/windows/wsl/install) (for Windows users)
- OpenWeatherMap API key (free at [openweathermap.org](https://openweathermap.org/api))

### 1. Clone & Setup

```bash
git clone https://github.com/YOUR_USERNAME/weather-etl-pipeline.git
cd weather-etl-pipeline
```

### 2. Add Your API Key

Create a `.env` file:
```bash
cp .env.example .env
```

Edit `.env`:
```
API_KEY=your_openweather_api_key_here

DB_HOST=postgres
DB_PORT=5432
DB_NAME=weather_db
DB_USER=weather_user
DB_PASSWORD=weather
```

### 3. Start Everything

```bash
docker compose up -d
```

This starts:
- ✅ PostgreSQL (port 5433)
- ✅ MinIO (port 9000 / console 9001)
- ✅ Apache Airflow (port 8081)
- ✅ Weather ETL pipeline

### 4. Trigger the Pipeline

Open Airflow UI:
```
http://localhost:8081
```
- **Username:** `admin`
- **Password:** `admin`

Toggle the DAG **ON**, then click the **▶️ Play** button to trigger manually.

The pipeline will then run automatically every hour.

---

## ✅ Verification

### Check Bronze Layer (MinIO)
```bash
# Or open browser: http://localhost:9001 (minioadmin / minioadmin)
docker exec weather-etl python -c "
from minio import Minio
client = Minio('minio:9000', access_key='minioadmin', secret_key='minioadmin', secure=False)
objects = list(client.list_objects('bronze', prefix='weather/', recursive=True))
print(f'{len(objects)} raw JSON files in Bronze')
for obj in objects[-3:]:
    print(f'  {obj.object_name}')
"
```

### Check Silver Layer (Delta Lake)
```bash
# Delta table files on local disk
ls -la data/silver/weather/_delta_log/
```

### Check Gold Tables (PostgreSQL)
```bash
docker exec -it weather-postgres psql -U weather_user -d weather_db -c "SELECT * FROM gold.gold_weather_summary;"
```

Expected output:
| city | total_readings | avg_temperature | min_temperature | max_temperature |
|------|---------------|----------------|----------------|----------------|
| Algiers | 5 | 25.85 | 25.66 | 26.13 |
| Paris | 5 | 33.81 | 30.79 | 36.19 |
| London | 5 | 29.62 | 28.01 | 31.09 |

---

## 📁 Project Structure

```
weather-etl-pipeline/
│
├── .env                          # API key & DB credentials (gitignored)
├── .env.example                  # Template for .env
├── .dockerignore                 # Files Docker should ignore
├── docker-compose.yml            # Orchestrates all services
├── Dockerfile                    # Python app container
├── requirements.txt              # Python dependencies
├── wait-for-db.py                # Waits for PostgreSQL before running
│
├── app/                          # Python ETL code
│   ├── extract.py                # Fetches weather from OpenWeatherMap API
│   ├── bronze.py                 # Saves raw JSON to MinIO
│   ├── silver.py                 # Spark + Delta Lake cleaning & enrichment
│   ├── load.py                   # Loads Silver data to PostgreSQL
│   └── main.py                   # Manual pipeline runner
│
├── dags/                         # Airflow DAGs
│   └── weather_etl_dag.py       # Full pipeline workflow (5 tasks)
│
├── dbt/                          # dbt SQL transformations
│   ├── dbt_project.yml           # dbt project config
│   ├── profiles.yml              # PostgreSQL connection for dbt
│   └── models/
│       ├── sources.yml           # Source table definitions
│       └── gold/
│           ├── gold_daily_weather.sql      # Daily city averages
│           └── gold_weather_summary.sql    # City-level summary stats
│
├── airflow/                      # Custom Airflow image
│   └── Dockerfile                # Installs Spark, Delta, dbt inside Airflow
│
├── data/                         # Delta Lake tables (auto-created, gitignored)
│   └── silver/
│       └── weather/
│           └── _delta_log/       # Delta transaction history
│
└── images/                       # Screenshots for README
    └── powerbi_dashboard.png     # Your Power BI dashboard (add yours!)
```

---

## 🔄 Data Flow

```
1. EXTRACT    → Call OpenWeatherMap API (London, Paris, Algiers)
2. BRONZE     → Save raw JSON to MinIO (timestamped, untouched)
3. SILVER     → Spark cleans data:
                 • Cast types (string → double, int)
                 • Convert Unix timestamp → datetime
                 • Add temp_category (cold/mild/hot)
                 • Add humidity_level (dry/comfortable/humid)
                 • Write as Delta Lake (ACID + history)
4. LOAD       → Read Silver Delta, load to PostgreSQL
5. GOLD (dbt) → SQL transformations:
                 • gold_daily_weather: daily avg/min/max per city
                 • gold_weather_summary: city-level KPIs
6. VISUALIZE  → Power BI connects to PostgreSQL → dashboards
```

---

## 🎯 Key Features Demonstrated

| Feature | Where | Why It Matters |
|---------|-------|----------------|
| **Medallion Architecture** | Entire pipeline | Industry-standard data layering (Bronze/Silver/Gold) |
| **ACID Transactions** | Delta Lake Silver | Reliable writes, no corrupted data |
| **Time Travel** | `DESCRIBE HISTORY delta.\`path\`` | Query historical versions, recover mistakes |
| **Schema Enforcement** | Delta Lake Silver | Catches bad data early |
| **Data Quality** | dbt tests (ready to add) | Validates business logic |
| **Orchestration** | Airflow DAGs | Production scheduling, retries, monitoring |
| **Containerization** | Docker Compose | Reproducible, portable, no "works on my machine" |
| **SQL Transformations** | dbt Gold layer | Analytics engineering best practice |

---

## 📊 Power BI Dashboard

Connect Power BI Desktop to PostgreSQL:

| Setting | Value |
|---------|-------|
| Server | `localhost:5433` |
| Database | `weather_db` |
| Username | `weather_user` |
| Password | `weather` |

Load these tables:
- `gold.gold_daily_weather`
- `gold.gold_weather_summary`

Build visuals:
- 🌡️ Average Temperature by City (Bar Chart)
- 📈 Daily Temperature Trends (Line Chart)
- 📊 Total Readings (Card)
- 💧 Humidity vs Temperature (Scatter Plot)

> **Screenshot your dashboard and save it to `images/powerbi_dashboard.png`!**

---

## 🛣️ Roadmap

- [x] Docker + Docker Compose setup
- [x] MinIO Bronze layer (S3-compatible data lake)
- [x] Apache Airflow orchestration (hourly scheduling)
- [x] Apache Spark + Delta Lake Silver layer
- [x] dbt Gold layer (SQL transformations)
- [x] PostgreSQL data warehouse
- [x] Power BI dashboard connection
- [ ] Add dbt tests (data quality)
- [ ] Add Great Expectations for data validation
- [ ] Add Spark Streaming for real-time ingestion
- [ ] Deploy to cloud (AWS/GCP/Azure)
- [ ] Add CI/CD with GitHub Actions

---

## 🙋 About Me

I'm a fresh graduate Data Engineer building real-world projects to learn and showcase skills in modern data architecture. This project is my hands-on deep-dive into:

- **Data Orchestration** with Apache Airflow
- **Big Data Processing** with Apache Spark
- **Reliable Storage** with Delta Lake
- **Analytics Engineering** with dbt
- **Data Visualization** with Power BI

**Connect with me:**
- LinkedIn: https://www.linkedin.com/in/negad-youcef-3110b0277/
- Email: mrnegadyoucef@gmail.com

---

## 📚 References

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Delta Lake Documentation](https://docs.delta.io/)
- [dbt Documentation](https://docs.getdbt.com/)
- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [MinIO Documentation](https://min.io/docs/minio/linux/index.html)
