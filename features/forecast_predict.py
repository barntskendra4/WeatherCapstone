import requests
from datetime import datetime
from core.weather_api import WeatherAPIError

class ForecastPredict:
    """Handles weather forecast predictions and analysis"""
    
    def __init__(self, weather_api):
        self.api = weather_api
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
    
    def get_5_day_forecast(self, city, state=None):
        """Get 5-day weather forecast for a city with optional state parameter
        
        Args:
            city (str): The city name for the weather forecast
            state (str, optional): The state/region abbreviation (e.g., 'CA', 'TX')
        
        Returns:
            str: Formatted 5-day weather forecast text
        """
        try:
            # Validate API key first
            if not self.api.api_key:
                raise WeatherAPIError("API key not configured properly")

            # Build location query with optional state parameter
            location_query = city
            if state:
                location_query = f"{city},{state}"
            
            url = f"{self.forecast_url}?q={location_query}&appid={self.api.api_key}&units=imperial"
            
            try:
                response = requests.get(url, timeout=10)
            except requests.exceptions.Timeout:
                raise WeatherAPIError("Request timed out. Please check your internet connection.")
            except requests.exceptions.ConnectionError:
                raise WeatherAPIError("Network connection error. Please check your internet connection.")
            
            if response.status_code == 401:
                raise WeatherAPIError("Invalid API key for forecast service")
            elif response.status_code == 404:
                raise KeyError("City not found")
            elif response.status_code != 200:
                raise WeatherAPIError(f"Forecast API returned status {response.status_code}")
            
            forecast_data = response.json()
            
            return self._process_forecast_data(forecast_data)
            
        except (KeyError, WeatherAPIError):
            # Re-raise these specific exceptions
            raise
        except Exception as e:
            raise WeatherAPIError(f"Error getting forecast: {str(e)}")
    
    def _process_forecast_data(self, data):
        """Process raw forecast data into a readable format"""
        forecast_list = data['list']
        city_name = data['city']['name']
        
        # Group forecasts by day
        daily_forecasts = {}
        
        for item in forecast_list[:40]:  # 5 days * 8 (3-hour intervals)
            # Convert timestamp to datetime
            dt = datetime.fromtimestamp(item['dt'])
            date_key = dt.strftime('%Y-%m-%d')
            
            if date_key not in daily_forecasts:
                daily_forecasts[date_key] = []
            
            forecast_item = {
                'time': dt.strftime('%H:%M'),
                'temp': item['main']['temp'],
                'description': item['weather'][0]['description'],
                'humidity': item['main']['humidity'],
                'feels_like': item['main']['feels_like']
            }
            
            daily_forecasts[date_key].append(forecast_item)
        
        return self._format_forecast_display(city_name, daily_forecasts)
    
    def _format_forecast_display(self, city, daily_forecasts):
        """Format forecast data for display"""
        result = f"5-Day Weather Forecast for {city}\n"
        result += "=" * 50 + "\n\n"
        
        for date_str, forecasts in sorted(daily_forecasts.items())[:5]:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            day_name = date_obj.strftime('%A, %B %d')
            
            result += f"📅 {day_name}\n"
            result += "-" * 30 + "\n"
            
            # Calculate daily summary
            temps = [f['temp'] for f in forecasts]
            high_temp = max(temps)
            low_temp = min(temps)
            
            # Get most common weather description
            descriptions = [f['description'] for f in forecasts]
            most_common_desc = max(set(descriptions), key=descriptions.count)
            
            result += f"🌡️ High: {high_temp:.0f}°F | Low: {low_temp:.0f}°F\n"
            result += f"☁️ Conditions: {most_common_desc.title()}\n"
            
            # Show a few time points
            result += "⏰ Hourly Details:\n"
            for i, forecast in enumerate(forecasts[::2]):  # Every 6 hours
                if i >= 4:  # Limit to 4 entries per day
                    break
                result += f"   {forecast['time']}: {forecast['temp']:.0f}°F, {forecast['description']}\n"
            
            result += "\n"
        
        return result
