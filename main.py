# Main app logic
# This is the entry point for your weather dashboard application
from config import WEATHER_API_KEY, WeatherAPI

class WeatherDashboard:
    """Main application controller"""
    
    def __init__(self):
        self.api = WeatherAPI(WEATHER_API_KEY)

if __name__ == "__main__":
    weather_app = WeatherDashboard()
    weather_app.run()