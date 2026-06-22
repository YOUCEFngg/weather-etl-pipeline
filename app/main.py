from extract import get_weather
from load import load_data

cities = ["London", "Paris", "Algiers"]

records = [get_weather(city) for city in cities]

load_data(records)

print("Data loaded successfully")