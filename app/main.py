from extract import get_weather
from bronze import save_to_bronze
from load import load_data

cities = ["London", "Paris", "Algiers"]

# Extract raw data from API
records = [get_weather(city) for city in cities]
print(f"Extracted data for {len(records)} cities")

# Save to Bronze layer (MinIO) — raw, untouched
save_to_bronze(records)

# Load to PostgreSQL
load_data(records)

print("Pipeline completed successfully!")
