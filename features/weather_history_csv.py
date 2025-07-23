"""
Enhanced weather history management that works with CSV format

This module provides a WeatherHistoryCSV class that manages weather history data
in a structured CSV format, making it easy to store, retrieve, and analyze
weather information over time.

Features:
- Automatic CSV file creation and management
- Adding new weather records with timestamps
- Retrieving recent weather history
- City-specific weather history
- Statistical analysis of weather data
- Error handling for file operations

Author: WeatherCap Development Team
Date: July 2025
"""

import csv
import os
from datetime import datetime

class WeatherHistoryCSV:
    """
    Manages weather history using CSV format for better organization and analysis.
    
    This class handles all aspects of weather history management including:
    - Creating and maintaining the CSV file structure
    - Adding new weather records with proper formatting
    - Retrieving historical data with various filtering options
    - Generating statistical summaries
    
    Attributes:
        history_file (str): Path to the CSV file storing weather history
        headers (list): Column headers for the CSV file structure
    """
    
    def __init__(self):
        """
        Initialize the WeatherHistoryCSV manager.
        
        Sets up the file path and CSV headers, then ensures the CSV file
        exists with proper structure.
        """
        # Define the path to the weather history CSV file
        self.history_file = "data/weather_history.csv"
        
        # Define the column structure for the CSV file
        # Date: YYYY-MM-DD format
        # Time: HH:MM:SS format (24-hour)
        # City: Name of the city
        # Temperature_F: Temperature in Fahrenheit
        # Description: Weather description (e.g., "clear sky", "light rain")
        # Humidity_Percent: Humidity percentage (0-100)
        self.headers = ['Date', 'Time', 'City', 'Temperature_F', 'Description', 'Humidity_Percent']
        
        # Ensure the CSV file exists and has proper headers
        self._ensure_csv_exists()
    
    def _ensure_csv_exists(self):
        """
        Ensure the CSV file exists with proper headers.
        
        Creates the data directory if it doesn't exist, and initializes
        the CSV file with column headers if the file is missing.
        This method is called during initialization to set up the file structure.
        
        Raises:
            Exception: If there are file system permission issues
        """
        try:
            # Create the data directory if it doesn't exist
            # exist_ok=True prevents error if directory already exists
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            
            # Check if the CSV file exists, if not create it with headers
            if not os.path.exists(self.history_file):
                with open(self.history_file, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    # Write the column headers as the first row
                    writer.writerow(self.headers)
        except Exception as e:
            print(f"Error creating CSV file: {e}")
    
    def add_weather_record(self, city, weather_data):
        """
        Add a new weather record to the CSV file.
        
        Takes weather data and appends it as a new row in the CSV file
        with the current timestamp. The temperature is rounded to the
        nearest integer for consistency.
        
        Args:
            city (str): Name of the city for this weather record
            weather_data (dict): Dictionary containing weather information with keys:
                - 'temperature': Temperature value (will be rounded to integer)
                - 'description': Weather description string
                - 'humidity': Humidity percentage value
        
        Example:
            weather_data = {
                'temperature': 75.3,
                'description': 'partly cloudy',
                'humidity': 65
            }
            add_weather_record('New York', weather_data)
        """
        try:
            # Get current timestamp for this record
            timestamp = datetime.now()
            date_str = timestamp.strftime('%Y-%m-%d')  # Format: 2025-07-20
            time_str = timestamp.strftime('%H:%M:%S')  # Format: 14:30:25
            
            # Prepare the record data as a list matching CSV headers
            record = [
                date_str,                                              # Date column
                time_str,                                              # Time column
                city,                                                  # City column
                str(int(round(weather_data['temperature']))),          # Temperature (rounded to int)
                weather_data['description'],                           # Description column
                str(weather_data['humidity'])                          # Humidity column
            ]
            
            # Append the new record to the CSV file
            with open(self.history_file, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(record)
                
        except Exception as e:
            print(f"Error adding weather record: {e}")
    
    def get_recent_history(self, limit=20):
        """
        Get recent weather history formatted for display.
        
        Retrieves the most recent weather records from the CSV file and
        formats them in a user-friendly way for display in the application.
        Records are shown in reverse chronological order (newest first).
        
        Args:
            limit (int, optional): Maximum number of records to retrieve.
                                 Defaults to 20.
        
        Returns:
            str: Formatted string containing recent weather history with
                 emojis and proper formatting, ready for display in the GUI.
                 Returns error message if file operations fail.
        
        Example output:
            📊 Recent Weather History (Last 3 records)
            ============================================================
            
            📅 2025-07-20 14:23:36
            🏙️  Miami: 91°F, scattered clouds, 66% humidity
            
            📅 2025-07-20 12:15:22
            🏙️  New York: 75°F, clear sky, 55% humidity
        """
        try:
            # Check if the CSV file exists
            if not os.path.exists(self.history_file):
                return "No weather history available."
            
            # Read all data from the CSV file
            with open(self.history_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader, None)  # Skip the header row
                data = list(reader)           # Load all data rows into memory
            
            # Handle case where file exists but has no data
            if not data:
                return "No weather history available."
            
            # Get the most recent records (last 'limit' entries)
            # If we have fewer records than the limit, use all available records
            recent_data = data[-limit:] if len(data) > limit else data
            recent_data.reverse()  # Show newest first (reverse chronological order)
            
            # Start building the formatted output string
            result = f"📊 Recent Weather History (Last {len(recent_data)} records)\n"
            result += "=" * 60 + "\n\n"
            
            # Process each weather record for display
            for row in recent_data:
                # Ensure the row has all expected columns (at least 6)
                if len(row) >= 6:
                    # Extract data from CSV columns
                    date = row[0]        # Date column
                    time = row[1]        # Time column
                    city = row[2]        # City column
                    temp = row[3]        # Temperature column
                    desc = row[4]        # Description column
                    humidity = row[5]    # Humidity column
                    
                    # Create timestamp string (include time if available)
                    timestamp = f"{date} {time}" if time else date
                    
                    # Format the weather information with emojis
                    result += f"📅 {timestamp}\n"
                    result += f"🏙️  {city}: {temp}°F, {desc}"
                    
                    # Add humidity if available (some old records might not have it)
                    if humidity:
                        result += f", {humidity}% humidity"
                    result += "\n\n"  # Add spacing between records
            
            return result
            
        except Exception as e:
            # Return error message if anything goes wrong with file operations
            return f"Error loading weather history: {e}"
    
    def get_city_history(self, city, limit=10):
        """
        Get weather history for a specific city.
        
        Filters the weather history to show only records for a particular city.
        The city name comparison is case-insensitive for better user experience.
        
        Args:
            city (str): Name of the city to filter by (case-insensitive)
            limit (int, optional): Maximum number of records to return.
                                 Defaults to 10.
        
        Returns:
            str: Formatted string containing weather history for the specified city,
                 or appropriate message if no data is found.
        
        Example:
            get_city_history('Miami', 5)
            # Returns formatted history of last 5 Miami weather records
        """
        try:
            # Check if the CSV file exists
            if not os.path.exists(self.history_file):
                return f"No weather history available for {city}."
            
            # Read all data from CSV
            with open(self.history_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader, None)  # Skip header row
                data = list(reader)           # Load all data
            
            # Filter records for the specified city (case-insensitive comparison)
            city_data = [row for row in data 
                        if len(row) >= 3 and row[2].lower() == city.lower()]
            
            # Handle case where no records found for this city
            if not city_data:
                return f"No weather history found for {city}."
            
            # Get the most recent records for this city
            recent_city_data = city_data[-limit:] if len(city_data) > limit else city_data
            recent_city_data.reverse()  # Show newest first
            
            # Build formatted output
            result = f"📊 Weather History for {city.title()}\n"
            result += "=" * 40 + "\n\n"
            
            # Format each record for display
            for row in recent_city_data:
                date = row[0]                                    # Date column
                time = row[1]                                    # Time column
                temp = row[3]                                    # Temperature column
                desc = row[4]                                    # Description column
                humidity = row[5] if len(row) > 5 else ""       # Humidity (if available)
                
                # Create timestamp (include time if available)
                timestamp = f"{date} {time}" if time else date
                
                # Format the record
                result += f"📅 {timestamp}: {temp}°F, {desc}"
                if humidity:
                    result += f", {humidity}% humidity"
                result += "\n"
            
            return result
            
        except Exception as e:
            return f"Error loading city history: {e}"
    
    def get_statistics(self):
        """
        Get comprehensive weather statistics from all historical data.
        
        Analyzes all weather records in the CSV file to generate statistical
        summaries including temperature ranges, averages, humidity data,
        and city tracking information.
        
        Returns:
            str: Formatted string containing detailed weather statistics
                 including:
                 - Total number of records
                 - Number of unique cities tracked
                 - List of all cities
                 - Temperature statistics (min, max, average)
                 - Humidity statistics (where available)
        
        Note:
            This method processes all historical data, so performance may
            be slower with very large datasets.
        """
        try:
            # Check if CSV file exists
            if not os.path.exists(self.history_file):
                return "No weather data available for statistics."
            
            # Read all data from CSV file
            with open(self.history_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader, None)  # Skip header row
                data = list(reader)           # Load all data into memory
            
            # Handle empty file case
            if not data:
                return "No weather data available for statistics."
            
            # Calculate basic statistics
            total_records = len(data)
            
            # Get unique cities from the data (case-sensitive for accuracy)
            cities = set(row[2] for row in data if len(row) >= 3)
            
            # Initialize lists for numerical analysis
            temps = []           # Store all temperature values
            humidity_values = [] # Store all humidity values
            
            # Process each record to extract numerical data
            for row in data:
                # Extract temperature data (column index 3)
                if len(row) >= 4 and row[3]:
                    try:
                        temps.append(float(row[3]))
                    except ValueError:
                        # Skip records with invalid temperature data
                        pass
                
                # Extract humidity data (column index 5)
                if len(row) >= 6 and row[5]:
                    try:
                        humidity_values.append(float(row[5]))
                    except ValueError:
                        # Skip records with invalid humidity data
                        pass
            
            # Build the statistics report
            result = f"📊 Weather History Statistics\n"
            result += "=" * 40 + "\n\n"
            
            # Basic count statistics
            result += f"📈 Total Records: {total_records}\n"
            result += f"🏙️  Cities Tracked: {len(cities)}\n"
            result += f"🌍 Cities: {', '.join(sorted(cities))}\n\n"
            
            # Temperature statistics (if we have valid temperature data)
            if temps:
                avg_temp = sum(temps) / len(temps)    # Calculate average
                min_temp = min(temps)                 # Find minimum
                max_temp = max(temps)                 # Find maximum
                
                result += f"🌡️  Temperature Range: {min_temp:.1f}°F - {max_temp:.1f}°F\n"
                result += f"🌡️  Average Temperature: {avg_temp:.1f}°F\n"
            
            # Humidity statistics (if we have valid humidity data)
            if humidity_values:
                avg_humidity = sum(humidity_values) / len(humidity_values)
                result += f"💧 Average Humidity: {avg_humidity:.1f}%\n"
            
            return result
            
        except Exception as e:
            return f"Error calculating statistics: {e}"

# Example usage and testing
if __name__ == "__main__":
    """
    Example usage demonstration of the WeatherHistoryCSV class.
    
    This section runs when the file is executed directly and demonstrates
    how to use the main functionality of the class. It's useful for testing
    and as documentation for developers.
    """
    # Create an instance of the weather history manager
    history = WeatherHistoryCSV()
    
    # Display recent weather history (last 10 records)
    print("=== RECENT WEATHER HISTORY ===")
    print(history.get_recent_history(10))
    
    # Add a separator for clarity
    print("\n" + "="*50 + "\n")
    
    # Display comprehensive weather statistics
    print("=== WEATHER STATISTICS ===")
    print(history.get_statistics())
