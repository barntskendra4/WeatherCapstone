#!/usr/bin/env python3
"""
Test the fixed 5-day forecast with state input functionality
"""

import sys
import os

# Add the current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_forecast_state_input():
    """Test the 5-day forecast with state input"""
    print("🧪 Testing 5-Day Forecast with State Input")
    print("=" * 50)
    
    try:
        from core.weather_api import WeatherAPI
        from features.forecast_predict import ForecastPredict
        
        # Initialize API and forecast
        api = WeatherAPI()
        forecast = ForecastPredict(api)
        
        # Test cases
        test_cases = [
            ("Miami", "FL"),
            ("Portland", "OR"),
            ("Austin", "TX"),
            ("Boston", "MA"),
            ("Chicago", None)  # Test without state
        ]
        
        for city, state in test_cases:
            print(f"\n🌤️ Testing: {city}" + (f", {state}" if state else ""))
            print("-" * 30)
            
            try:
                result = forecast.get_5_day_forecast(city, state)
                if result:
                    # Show first few lines of the result
                    lines = result.split('\n')
                    print("✅ SUCCESS!")
                    print("Preview:")
                    for line in lines[:5]:
                        print(f"  {line}")
                    print("  ...")
                else:
                    print("❌ No result returned")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_forecast_state_input()
    print(f"\n{'🎉 TESTING COMPLETED!' if success else '💥 TESTING FAILED!'}")
    print("\nNow try the forecast feature in the GUI with state input!")
