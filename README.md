# Weather ETL Pipeline

An automated end-to-end Data Engineering pipeline that Extracts, Transforms, and Loads (ETL) historical or live weather data from an external API into a structured database for analytics and visualization. 

## 📌 Project Overview
This repository implements a production-ready ETL architecture designed to collect weather conditions (temperature, wind speed, humidity, etc.), clean and normalize the payload, and persist the records into a relational or cloud-based data store. The entire workflow is automated and orchestrated.

## 🏗️ Architecture & Flow
1. **Extract**: Fetch real-time/forecast weather data from a REST API (e.g., OpenWeatherMap / Open-Meteo) using API keys or geolocation endpoints.
2. **Transform**: 
   - Parse JSON responses into clean tabular/structured formats using Python (Pandas/PySpark).
   - Convert timestamps (e.g., UTC to local time).
   - Filter unnecessary data, handle missing fields, and enforce data schemas.
3. **Load**: Ingest the processed data into a destination warehouse/database for downstream consumption.

## 🛠️ Tech Stack
- **Language:** Python 3.2
- **Orchestration / Scheduling:** Apache Airflow / Cron jobs
- **Data Manipulation:** Pandas / NumPy
- **Database:** PostgreSQL 
- **Containerization:** Docker & Docker Compose
├── .env.example           # Example file for environment variables
├── docker-compose.yaml    # Docker setup for Airflow/Database environments
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
