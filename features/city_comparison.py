from datetime import datetime

class CityComparison:
    """Handles comparison between cities"""
    
    def __init__(self, weather_api):
        self.api = weather_api
    
    def compare_cities(self, city1, city2):
        """Compare weather between two cities and return formatted results"""
        try:
            # Get weather data for both cities
            weather1 = self.api.get_weather_from_api(city1)
            weather2 = self.api.get_weather_from_api(city2)
            
            # Format the comparison results
            comparison_result = self._format_comparison(city1, weather1, city2, weather2)
            
            return comparison_result
            
        except Exception as e:
            return f"Error comparing cities: {str(e)}"
    
    def _format_comparison(self, city1, weather1, city2, weather2):
        """Format the comparison results into a readable string"""
        result = f"Weather Comparison - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        result += "=" * 60 + "\n\n"
        
        # City 1 details
        result += f"🏙️ {city1.upper()}\n"
        result += f"   Temperature: {weather1['temperature']:.1f}°F\n"
        result += f"   Condition: {weather1['description'].title()}\n"
        result += f"   Humidity: {weather1['humidity']}%\n\n"
        
        # City 2 details
        result += f"🏙️ {city2.upper()}\n"
        result += f"   Temperature: {weather2['temperature']:.1f}°F\n"
        result += f"   Condition: {weather2['description'].title()}\n"
        result += f"   Humidity: {weather2['humidity']}%\n\n"
        
        # Comparison analysis
        result += "📊 COMPARISON ANALYSIS\n"
        result += "-" * 30 + "\n"
        
        # Temperature comparison
        temp_diff = weather1['temperature'] - weather2['temperature']
        if abs(temp_diff) < 1:
            result += f"🌡️ Temperature: Similar temperatures (difference: {abs(temp_diff):.1f}°F)\n"
        elif temp_diff > 0:
            result += f"🌡️ Temperature: {city1} is {temp_diff:.1f}°F warmer than {city2}\n"
        else:
            result += f"🌡️ Temperature: {city2} is {abs(temp_diff):.1f}°F warmer than {city1}\n"
        
        # Humidity comparison
        humidity_diff = weather1['humidity'] - weather2['humidity']
        if abs(humidity_diff) < 5:
            result += f"💧 Humidity: Similar humidity levels (difference: {abs(humidity_diff)}%)\n"
        elif humidity_diff > 0:
            result += f"💧 Humidity: {city1} is {humidity_diff}% more humid than {city2}\n"
        else:
            result += f"💧 Humidity: {city2} is {abs(humidity_diff)}% more humid than {city1}\n"
        
        # Weather condition comparison
        if weather1['description'].lower() == weather2['description'].lower():
            result += f"☁️ Conditions: Both cities have similar weather ({weather1['description']})\n"
        else:
            result += f"☁️ Conditions: {city1} has {weather1['description']}, {city2} has {weather2['description']}\n"
        
        # Recommendations
        result += "\n💡 RECOMMENDATIONS\n"
        result += "-" * 20 + "\n"
        
        if weather1['temperature'] > weather2['temperature']:
            result += f"🌞 For warmer weather, choose {city1}\n"
            result += f"❄️ For cooler weather, choose {city2}\n"
        else:
            result += f"🌞 For warmer weather, choose {city2}\n"
            result += f"❄️ For cooler weather, choose {city1}\n"
        
        if weather1['humidity'] < weather2['humidity']:
            result += f"🏜️ For lower humidity, choose {city1}\n"
        else:
            result += f"🏜️ For lower humidity, choose {city2}\n"
        
        return result
