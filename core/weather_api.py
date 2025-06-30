import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables (loaded from .env file)
WEATHER_API_KEY = os.getenv("api_key")
API_BASE_URL = "https://api.openweathermap.org/data/2.5"


class WeatherAPI:
    def __init__(self, api_key: str = None):
        # Use provided API key or fall back to the one from .env
        self.api_key = api_key or WEATHER_API_KEY
        self.api_base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def get_weather_from_api(self, city_name):
        # Build the complete URL for the API request
        api_url = f"{self.api_base_url}?q={city_name}&appid={self.api_key}&units=imperial"
        
        # Make the request to the API (this might fail if no internet)
        response = requests.get(api_url) 
        
        # Check if the request was successful
        if response.status_code == 404:
            raise KeyError("City not found")
        elif response.status_code != 200:
            raise requests.exceptions.RequestException(f"API returned status {response.status_code}")
        
        # Convert the response to a Python dictionary
        weather_data = response.json()
        
        # Extract the information we need (renamed from confusing single letters)
        temperature = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        
        return {
            'temperature': temperature,
            'description': description,
            'humidity': humidity
        }