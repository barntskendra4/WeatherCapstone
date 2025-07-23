"""
WeatherCap Application Entry Point
Simplified main.py with separation of concerns implementation
"""

from app_controller import WeatherAppController
from core.weather_api import WeatherAPIError


def main():
    """Main application entry point"""
    try:
        # Create and run the weather application
        weather_app = WeatherAppController()
        weather_app.run()
        
    except WeatherAPIError as e:
        print(f"Failed to start application due to API configuration: {e}")
    except Exception as e:
        print(f"Unexpected error starting application: {e}")


if __name__ == "__main__":
    main()
