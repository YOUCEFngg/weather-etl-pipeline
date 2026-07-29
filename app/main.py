from extract import get_weather
from bronze import save_to_bronze
from silver import bronze_to_silver
from load import load_data

cities = ["London", "Paris", "Algiers"]

# 1. EXTRACT — fetch from API
records = [get_weather(city) for city in cities]
print(f"Extracted data for {len(records)} cities")

# 2. BRONZE — save raw JSON to MinIO
save_to_bronze(records)

# 3. SILVER — Spark + Delta Lake processing
bronze_to_silver(records)

# 4. LOAD — read Silver, load to PostgreSQL
load_data()

print("\n Full pipeline completed: API → Bronze → Silver → PostgreSQL")
