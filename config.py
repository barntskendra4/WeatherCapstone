# Your API keys
# Store your weather API keys and other configuration here

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables (loaded from .env file)
WEATHER_API_KEY = os.getenv("api_key")
API_BASE_URL = "https://api.openweathermap.org/data/2.5"

# Application settings
DEFAULT_UNITS = "imperial"  # Fahrenheit
DEFAULT_CITY = "New Brunswick"

# GUI settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
DEFAULT_THEME = "light"


