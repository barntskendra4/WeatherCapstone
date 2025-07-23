import os
import requests
from dotenv import load_dotenv
import re

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables (loaded from .env file)
WEATHER_API_KEY = os.getenv("api_key")
API_BASE_URL = "https://api.openweathermap.org/data/2.5"


class WeatherAPIError(Exception):
    """Custom exception for Weather API errors"""
    pass


class WeatherAPI:
    _SENTINEL = object()  # Sentinel value to distinguish between None and default
    
    def __init__(self, api_key = _SENTINEL):
        # If no parameter provided, use .env key
        # If None or empty string explicitly provided, use that value
        if api_key is self._SENTINEL:
            self.api_key = WEATHER_API_KEY
        else:
            self.api_key = api_key
        self.api_base_url = "https://api.openweathermap.org/data/2.5/weather"
        
        # Validate API key during initialization
        self._validate_api_key()
    
    def _validate_api_key(self):
        """Validate the API key format and existence"""
        # Check if API key is None or empty
        if self.api_key is None:
            raise WeatherAPIError(
                "API key not found. Please ensure you have:\n"
                "1. Created a .env file in the project root\n"
                "2. Added your OpenWeatherMap API key as: api_key=YOUR_API_KEY\n"
                "3. Obtained a valid API key from https://openweathermap.org/api"
            )
        
        # Check if API key is empty string or just whitespace
        if not self.api_key or not self.api_key.strip():
            raise WeatherAPIError(
                "API key is empty. Please check your .env file and ensure it contains a valid API key."
            )
        
        # Basic format validation for OpenWeatherMap API key (32 character alphanumeric)
        if not re.match(r'^[a-zA-Z0-9]{32}$', self.api_key.strip()):
            raise WeatherAPIError(
                "Invalid API key format. OpenWeatherMap API keys should be 32 characters long and contain only letters and numbers.\n"
                "Please check your API key at https://openweathermap.org/api"
            )
    
    def get_weather_from_api(self, city_name, state=None, country=None):
        """
        Get weather data from OpenWeatherMap API with comprehensive error handling
        
        Args:
            city_name (str): Name of the city
            state (str, optional): State code (for US cities) or state name
            country (str, optional): Country code (ISO 3166-1 alpha-2)
        
        Returns:
            dict: Weather data containing temperature, description, and humidity
            
        Examples:
            get_weather_from_api("Miami")  # Miami (could be any Miami)
            get_weather_from_api("Miami", "FL")  # Miami, Florida specifically
            get_weather_from_api("Miami", "Florida")  # Miami, Florida (full state name)
            get_weather_from_api("Paris", country="FR")  # Paris, France
        """
        try:
            # Validate inputs
            if not city_name or not city_name.strip():
                raise ValueError("City name cannot be empty")
            
            # Build the location query string
            location_query = city_name.strip()
            
            # Add state if provided (works for US locations)
            if state:
                state_clean = state.strip()
                # Handle both state codes (FL) and full names (Florida)
                location_query += f",{state_clean}"
                
                # If state is provided but no country, assume US for better API results
                if not country:
                    country = "US"
            
            # Add country if provided
            if country:
                country_clean = country.strip()
                location_query += f",{country_clean}"
            
            # Build the complete URL for the API request
            api_url = f"{self.api_base_url}?q={location_query}&appid={self.api_key}&units=imperial"
            
            # Make the request to the API with timeout
            try:
                response = requests.get(api_url, timeout=10)
            except requests.exceptions.Timeout:
                raise WeatherAPIError("Request timed out. Please check your internet connection and try again.")
            except requests.exceptions.ConnectionError:
                raise WeatherAPIError("Network connection error. Please check your internet connection.")
            except requests.exceptions.RequestException as e:
                raise WeatherAPIError(f"Network error occurred: {str(e)}")
            
            # Handle different HTTP status codes
            if response.status_code == 401:
                raise WeatherAPIError(
                    "Invalid API key. Please check your OpenWeatherMap API key.\n"
                    "Make sure:\n"
                    "1. Your API key is correct in the .env file\n"
                    "2. Your API key is active (new keys may take up to 2 hours to activate)\n"
                    "3. You have API calls remaining in your plan"
                )
            elif response.status_code == 404:
                raise KeyError(f"Location '{location_query}' not found. Please check the spelling and try again.")
            elif response.status_code == 429:
                raise WeatherAPIError(
                    "API rate limit exceeded. Please wait a moment and try again, or upgrade your OpenWeatherMap plan."
                )
            elif response.status_code == 500:
                raise WeatherAPIError("OpenWeatherMap server error. Please try again later.")
            elif response.status_code != 200:
                raise WeatherAPIError(f"API request failed with status {response.status_code}: {response.text}")
            
            # Parse JSON response
            try:
                weather_data = response.json()
            except ValueError as e:
                raise WeatherAPIError(f"Invalid response format from API: {str(e)}")
            
            # Validate response structure
            if 'main' not in weather_data or 'weather' not in weather_data:
                raise WeatherAPIError("Invalid response structure from API")
            
            if not weather_data['weather'] or 'description' not in weather_data['weather'][0]:
                raise WeatherAPIError("Missing weather description in API response")
            
            # Extract the information we need with error handling
            try:
                temperature = weather_data['main']['temp']
                description = weather_data['weather'][0]['description']
                humidity = weather_data['main']['humidity']
                
                return {
                    'temperature': temperature,
                    'description': description,
                    'humidity': humidity
                }
            except KeyError as e:
                raise WeatherAPIError(f"Missing expected data in API response: {str(e)}")
                
        except (KeyError, ValueError) as e:
            # Re-raise these specific exceptions without wrapping
            raise
        except WeatherAPIError:
            # Re-raise our custom exceptions
            raise
        except Exception as e:
            # Catch any other unexpected errors
            raise WeatherAPIError(f"Unexpected error occurred: {str(e)}")