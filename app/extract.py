import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

cities = ["London", "Paris", "Algiers"]

def get_weather(city):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    return {
        "city": city,
        "timestamp": data["dt"],
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "weather_description": data["weather"][0]["description"]
    }