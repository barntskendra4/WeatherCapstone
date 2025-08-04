from tkinter import messagebox, filedialog
from datetime import datetime
import requests
import os
import sys
from core.weather_api import WeatherAPIError
from utils.state_validator import StateValidator

# Add the features directory to the path to import groupFeature
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(current_dir)


class WeatherEventHandlers:
    """Handles all user interface events and interactions"""
    
    def __init__(self, weather_api, city_comparison, forecast_predict, weather_history):
        """
        Initialize event handlers with required service dependencies
        """
        self.api = weather_api
        self.city_comparison = city_comparison
        self.forecast_predict = forecast_predict
        self.weather_history = weather_history
        self.widgets = {}  # Will be set by the main application
        
        # Initialize state validator
        self.state_validator = StateValidator()
        
    def set_widgets(self, widgets):
        """Set widget references for event handling"""
        self.widgets = widgets
    
    def _is_zip_code(self, text):
        """Check if the input text is a zip code pattern"""
        import re
        # Remove any spaces and check patterns
        clean_text = text.replace(' ', '').replace('-', '')
        
        # US 5-digit zip code
        if re.match(r'^\d{5}$', clean_text):
            return True
        
        # US 9-digit zip code (with or without dash)
        if re.match(r'^\d{9}$', clean_text) or re.match(r'^\d{5}-\d{4}$', text):
            return True
        
        # Canadian postal code patterns (A1A 1A1 or A1A1A1)
        if re.match(r'^[A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d$', text):
            return True
        
        # UK postal code patterns (basic patterns)
        if re.match(r'^[A-Za-z]{1,2}\d{1,2}[A-Za-z]?\s?\d[A-Za-z]{2}$', text):
            return True
        
        return False
    
    def bind_events(self):
        """Bind all events to their respective handlers"""
        # Search events
        self.widgets['city_entry'].bind('<Return>', lambda e: self.handle_search_weather())
        self.widgets['state_entry'].bind('<Return>', lambda e: self.handle_search_weather())
        self.widgets['search_btn'].configure(command=self.handle_search_weather)
        
        # Theme events
        self.widgets['theme_switch'].configure(command=self.handle_theme_toggle)
        
        # City comparison events
        self.widgets['city1_entry'].bind('<Return>', lambda e: self.handle_compare_cities())
        self.widgets['state1_entry'].bind('<Return>', lambda e: self.handle_compare_cities())
        self.widgets['city2_entry'].bind('<Return>', lambda e: self.handle_compare_cities())
        self.widgets['state2_entry'].bind('<Return>', lambda e: self.handle_compare_cities())
        self.widgets['compare_btn'].configure(command=self.handle_compare_cities)
        
        # Forecast events
        self.widgets['forecast_city_entry'].bind('<Return>', lambda e: self.handle_get_forecast())
        self.widgets['forecast_state_entry'].bind('<Return>', lambda e: self.handle_get_forecast())
        self.widgets['forecast_btn'].configure(command=self.handle_get_forecast)
        
        # History events
        self.widgets['recent_btn'].configure(command=self.handle_load_recent_history)
        self.widgets['stats_btn'].configure(command=self.handle_load_history_statistics)
        
        # Group feature events
        self.widgets['csv_comparison_btn'].configure(command=self.handle_csv_comparison_only)
        self.widgets['live_csv_comparison_btn'].configure(command=self.handle_live_csv_comparison)
        self.widgets['browse_csv_btn'].configure(command=self.handle_browse_csv_files)
        self.widgets['use_default_csv_btn'].configure(command=self.handle_use_default_csv)
        self.widgets['auto_detect_csv_btn'].configure(command=self.handle_auto_detect_csv)
        
        # Settings events
        self.widgets['save_btn'].configure(command=self.handle_save_preferences)
    
    def _validate_state_input(self, state_input):
        """
        Validate state input and provide user feedback for invalid states
        """
        if not state_input or not state_input.strip():
            return True, None
        
        is_valid, normalized_state, suggestion = self.state_validator.validate_state(state_input)
        
        if not is_valid:
            # Create error message with suggestion
            error_msg = f"Invalid state: '{state_input}'"
            if suggestion:
                error_msg += f"\n\nDid you mean: {suggestion}?"
            else:
                error_msg += f"\n\nPlease use standard state abbreviations (e.g., FL, CA, TX) or full state names."
            
            error_msg += f"\n\nExamples: FL, California, TX, New York"
            
            messagebox.showerror("Invalid State", error_msg)
            return False, None
        
        return True, normalized_state
    
    def handle_search_weather(self):
        """Handle weather search requests with state validation"""
        
        city = self.widgets['city_entry'].get().strip()
        state_input = self.widgets['state_entry'].get().strip() if self.widgets['state_entry'].get() else None
        
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name")
            return
        
        # Check if user entered a zip code instead of city name
        if self._is_zip_code(city):
            messagebox.showerror("Invalid Input", "Zip codes are not allowed. Please enter a city name instead.")
            return
        
        # Validate state input if provided
        if state_input:
            is_valid, normalized_state = self._validate_state_input(state_input)
            if not is_valid:
                return  # Stop execution if state is invalid
        else:
            normalized_state = None
        
        self.get_weather(city, normalized_state)
    
    def get_weather(self, city, state=None):
        """
        Get weather information for a city with optional state
        """
        try:
            # Create location display string
            location_display = city
            if state:
                location_display = f"{city}, {state}"
            
            self.widgets['status_label'].configure(text=f"Getting weather for {location_display}...")
            self.widgets['status_label'].update()
            
            weather_data = self.api.get_weather_from_api(city, state)
            
            # Update display
            self.widgets['city_label'].configure(text=location_display.title())
            self.widgets['temp_label'].configure(text=f"{weather_data['temperature']:.0f}°F")
            self.widgets['desc_label'].configure(text=weather_data['description'].title())
            self.widgets['humidity_label'].configure(text=f"{weather_data['humidity']}%")
            self.widgets['updated_label'].configure(text=datetime.now().strftime("%I:%M %p"))
            
            # Save to history (using the full location display)
            self._save_weather_to_history(location_display, weather_data)
            
            self.widgets['status_label'].configure(text=f"Weather updated for {location_display}")
            
        except KeyError as e:
            messagebox.showerror("Error", str(e))
            self.widgets['status_label'].configure(text="City not found")
        except WeatherAPIError as e:
            messagebox.showerror("API Error", str(e))
            self.widgets['status_label'].configure(text="API error")
        except ValueError as e:
            messagebox.showerror("Configuration Error", str(e))
            self.widgets['status_label'].configure(text="Configuration error")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"Network error: {str(e)}")
            self.widgets['status_label'].configure(text="Network error")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            self.widgets['status_label'].configure(text="Unexpected error")
    
    def handle_compare_cities(self):
        """Handle city comparison requests with state validation"""
        city1 = self.widgets['city1_entry'].get().strip()
        city2 = self.widgets['city2_entry'].get().strip()
        state1_input = self.widgets['state1_entry'].get().strip() if self.widgets['state1_entry'].get() else None
        state2_input = self.widgets['state2_entry'].get().strip() if self.widgets['state2_entry'].get() else None
        
        if not city1 or not city2:
            messagebox.showwarning("Warning", "Please enter both city names")
            return
        
        # Check if user entered zip codes instead of city names
        if self._is_zip_code(city1):
            messagebox.showerror("Invalid Input", f"Zip codes are not allowed. Please enter a city name instead of '{city1}'.")
            return
        
        if self._is_zip_code(city2):
            messagebox.showerror("Invalid Input", f"Zip codes are not allowed. Please enter a city name instead of '{city2}'.")
            return
        
        # Validate state inputs
        state1 = None
        state2 = None
        
        if state1_input:
            is_valid1, state1 = self._validate_state_input(state1_input)
            if not is_valid1:
                return  # Stop execution if first state is invalid
        
        if state2_input:
            is_valid2, state2 = self._validate_state_input(state2_input)
            if not is_valid2:
                return  # Stop execution if second state is invalid
        
        # Create location display strings
        location1 = f"{city1}, {state1}" if state1 else city1
        location2 = f"{city2}, {state2}" if state2 else city2
        
        try:
            self.widgets['status_label'].configure(text="Comparing cities...")
            comparison_result = self.city_comparison.compare_cities_with_states(
                city1, city2, state1, state2
            )
            
            self.widgets['comparison_textbox'].delete("0.0", "end")
            self.widgets['comparison_textbox'].insert("0.0", comparison_result)
            
            self.widgets['status_label'].configure(text=f"Compared {location1} and {location2}")
            
        except KeyError as e:
            messagebox.showerror("Error", str(e))
            self.widgets['status_label'].configure(text="City not found")
        except WeatherAPIError as e:
            messagebox.showerror("API Error", str(e))
            self.widgets['status_label'].configure(text="API error")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compare cities: {str(e)}")
            self.widgets['status_label'].configure(text="Error comparing cities")
    
    def handle_get_forecast(self):
        """Handle 5-day weather forecast requests with state validation"""
        city = self.widgets['forecast_city_entry'].get().strip()
        state_input = self.widgets['forecast_state_entry'].get().strip()
        
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name")
            return
        
        # Check if user entered a zip code instead of city name
        if self._is_zip_code(city):
            messagebox.showerror("Invalid Input", "Zip codes are not allowed. Please enter a city name instead.")
            return
        
        # Validate state input if provided
        state = None
        if state_input:
            is_valid, state = self._validate_state_input(state_input)
            if not is_valid:
                return  # Stop execution if state is invalid
        
        try:
            location_text = city
            if state:
                location_text = f"{city}, {state}"
            
            self.widgets['status_label'].configure(text=f"Getting 5-day forecast for {location_text}...")
            self.widgets['status_label'].update()
            
            forecast_result = self.forecast_predict.get_5_day_forecast(city, state)
            
            self.widgets['forecast_textbox'].delete("0.0", "end")
            self.widgets['forecast_textbox'].insert("0.0", forecast_result)
            
            self.widgets['status_label'].configure(text=f"5-day forecast for {location_text}")
            
        except WeatherAPIError as e:
            messagebox.showerror("API Error", str(e))
            self.widgets['status_label'].configure(text="API error")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get forecast: {str(e)}")
            self.widgets['status_label'].configure(text="Error getting forecast")
    
    def handle_load_recent_history(self):
        """Handle loading recent weather history"""
        try:
            history_content = self.weather_history.get_recent_history(20)
            self.widgets['history_textbox'].delete("0.0", "end")
            self.widgets['history_textbox'].insert("0.0", history_content)
        except Exception as e:
            self.widgets['history_textbox'].delete("0.0", "end")
            self.widgets['history_textbox'].insert("0.0", f"Error loading history: {e}")
    
    def handle_load_history_statistics(self):
        """Handle loading weather history statistics"""
        try:
            stats_content = self.weather_history.get_statistics()
            self.widgets['history_textbox'].delete("0.0", "end")
            self.widgets['history_textbox'].insert("0.0", stats_content)
        except Exception as e:
            self.widgets['history_textbox'].delete("0.0", "end")
            self.widgets['history_textbox'].insert("0.0", f"Error loading statistics: {e}")
    
    def handle_theme_toggle(self):
        """Handle theme toggle switch change"""
        # This will be called by the main application
        pass  # Implementation will be provided by main app
    
    def handle_save_preferences(self):
        """Handle save preferences requests"""
        # This will be called by the main application
        pass  # Implementation will be provided by main app
    
    def handle_csv_comparison_only(self):
        """Handle CSV comparison only request - groupCsvs only"""
        try:
            # Direct implementation to avoid import issues
            import pandas as pd
            import matplotlib.pyplot as plt
            import numpy as np
            
            # Always use groupCsvs folder only
            group_csv_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'groupCsvs')
            if not os.path.exists(group_csv_dir):
                group_csv_dir = "groupCsvs"
            
            if os.path.exists(group_csv_dir):
                csv_files = [os.path.join(group_csv_dir, f) 
                            for f in os.listdir(group_csv_dir) 
                            if f.endswith('.csv')]
                print(f"📁 Using {len(csv_files)} CSV files from groupCsvs folder only")
            else:
                self._update_group_status("❌ GroupCSV directory not found.")
                return
            
            self._update_group_status(f"📊 Creating CSV comparison for {len(csv_files)} files...")
            
            # Create the plot directly
            plt.figure(figsize=(14, 8))
            colors = plt.cm.Set1(np.linspace(0, 1, len(csv_files)))
            labels = [os.path.basename(f).replace('.csv', '') for f in csv_files]
            
            for i, (csv_file, label, color) in enumerate(zip(csv_files, labels, colors)):
                try:
                    df = pd.read_csv(csv_file)
                    
                    # Create datetime column if needed
                    if 'DateTime' not in df.columns and 'Date' in df.columns and 'Time' in df.columns:
                        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
                    
                    if 'DateTime' in df.columns:
                        df['DateTime'] = pd.to_datetime(df['DateTime'])
                        df = df.sort_values('DateTime')
                        x_data = df['DateTime']
                    else:
                        x_data = range(len(df))
                    
                    plt.plot(x_data, df['Temperature_F'], marker='o', markersize=4, 
                            linewidth=2, label=label, color=color, alpha=0.8)
                    
                    print(f"✅ Loaded {len(df)} records from {label}")
                    
                except Exception as e:
                    print(f"❌ Error loading {csv_file}: {e}")
                    continue
            
            plt.title("Historical Temperature Data Comparison", fontsize=16, fontweight='bold', pad=20)
            plt.xlabel("Date/Time", fontsize=12)
            plt.ylabel("Temperature (°F)", fontsize=12)
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            output_file = "group_csv_comparison.png"
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.show()
            self._update_group_status("✅ CSV comparison completed successfully!")
            
        except Exception as e:
            self._update_group_status(f"❌ Error during CSV comparison: {str(e)}")
            print(f"CSV comparison error: {e}")
    
    def handle_live_csv_comparison(self):
        """Handle CSV + Recent temperature comparison - groupCsvs only"""
        print("CSV + Recent Temps button clicked!")
        
        try:
            # Always use groupCsvs folder, ignore file selection
            group_csv_dir = "data/groupCsvs/"
            if not os.path.exists(group_csv_dir):
                group_csv_dir = "groupCsvs/"
            
            if os.path.exists(group_csv_dir):
                csv_files = [os.path.join(group_csv_dir, f) 
                            for f in os.listdir(group_csv_dir) 
                            if f.endswith('.csv')]
                print(f"📁 Using {len(csv_files)} CSV files from groupCsvs folder")
            else:
                print("❌ groupCsvs folder not found")
                return
            
            # Get cities for live data
            cities_text = self.widgets['live_cities_entry'].get().strip()
            if cities_text:
                raw_cities = [city.strip() for city in cities_text.split(',')]
                # Filter out zip codes and validate cities
                cities_for_live = []
                invalid_entries = []
                
                for city in raw_cities:
                    if self._is_zip_code(city):
                        invalid_entries.append(f"{city} (zip code not allowed)")
                    elif len(city) > 0:
                        cities_for_live.append(city)
                
                # Show error if zip codes were entered
                if invalid_entries:
                    error_msg = "❌ Zip codes not allowed. Please use city names only.\nInvalid entries: " + ", ".join(invalid_entries)
                    self._update_group_status(error_msg)
                    print(error_msg)
                    return
                
                # Show error if no valid cities after filtering
                if not cities_for_live:
                    error_msg = "❌ No valid city names provided. Please enter city names (not zip codes)."
                    self._update_group_status(error_msg)
                    print(error_msg)
                    return
            else:
                cities_for_live = ['Toronto', 'Lincoln', 'Rockland', 'Los Angeles']  # Default cities
            
            print(f"🌡️ Comparing groupCsv data with recent temps for: {', '.join(cities_for_live)}")
            
            # Use direct implementation instead of external function
            import pandas as pd
            import matplotlib.pyplot as plt
            import numpy as np
            from core.weather_api import WeatherAPI
            
            self._update_group_status(f"🌡️ Creating CSV + recent temperature comparison...")
            
            # Create the plot directly
            plt.figure(figsize=(16, 8))
            colors = plt.cm.Set1(np.linspace(0, 1, len(csv_files) + 1))
            labels = [os.path.basename(f).replace('.csv', '') for f in csv_files]
            
            # Plot CSV data
            for i, (csv_file, label, color) in enumerate(zip(csv_files, labels, colors[:-1])):
                try:
                    df = pd.read_csv(csv_file)
                    
                    # Create datetime column if needed
                    if 'DateTime' not in df.columns and 'Date' in df.columns and 'Time' in df.columns:
                        df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
                    
                    if 'DateTime' in df.columns:
                        df['DateTime'] = pd.to_datetime(df['DateTime'])
                        df = df.sort_values('DateTime')
                        x_data = df['DateTime']
                    else:
                        x_data = range(len(df))
                    
                    plt.plot(x_data, df['Temperature_F'], marker='o', markersize=4, 
                            linewidth=2, label=f'{label} (Historical)', color=color, alpha=0.8)
                    
                    print(f"✅ Loaded {len(df)} records from {label}")
                    
                except Exception as e:
                    print(f"❌ Error loading {csv_file}: {e}")
                    continue
            
            # Add recent weather data
            try:
                api = WeatherAPI()
                
                # Get recent weather data for each city
                for city in cities_for_live:
                    try:
                        # Get recent weather data (5 days of data points)
                        recent_data = api.get_recent_weather_data(city, days=5)
                        
                        if recent_data:
                            # Extract datetimes and temperatures
                            datetimes = [item['datetime'] for item in recent_data]
                            temps = [item['temperature'] for item in recent_data]
                            
                            # Plot recent weather data as a line
                            plt.plot(datetimes, temps, marker='s', markersize=5, 
                                    linewidth=2, linestyle='--', alpha=0.7,
                                    label=f'{city} (Recent Data)')
                            
                            print(f"✅ Plotted {len(recent_data)} recent data points for {city}")
                        else:
                            print(f"❌ No recent data available for {city}")
                            
                    except Exception as e:
                        print(f"❌ Error getting recent weather for {city}: {e}")
                        continue
                        
            except Exception as e:
                print(f"Error fetching recent weather: {e}")
            
            plt.title("GroupCSV Historical vs Recent Temperature Data", fontsize=16, fontweight='bold', pad=20)
            plt.xlabel("Date/Time", fontsize=12)
            plt.ylabel("Temperature (°F)", fontsize=12)
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            output_file = "group_live_csv_comparison.png"
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.show()
            
            self._update_group_status("✅ CSV + Recent temperature comparison completed successfully!")
            print("✅ GroupCSV comparison completed successfully!")
            
        except Exception as e:
            error_msg = f"❌ Error in CSV + Recent Temps comparison: {str(e)}"
            print(f"DEBUG: Full error details: {e}")
            import traceback
            traceback.print_exc()
            self._update_group_status(error_msg)
            messagebox.showerror("CSV + Recent Temps Error", error_msg)

    def handle_browse_csv_files(self):
        """Handle browse CSV files request"""
        try:
            filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
            files = filedialog.askopenfilenames(
                title="Select CSV files for comparison",
                filetypes=filetypes,
                initialdir=os.path.dirname(os.path.abspath(__file__))
            )
            
            if files:
                self.selected_csv_files = list(files)
                file_names = [os.path.basename(f) for f in files]
                self._update_group_status(f"📂 Selected {len(files)} CSV files:\n" + 
                                        "\n".join([f"  • {name}" for name in file_names]) +
                                        "\n\nNow click a comparison button to generate plots.")
            else:
                self._update_group_status("ℹ️ No files selected.")
                
        except Exception as e:
            error_msg = f"❌ Error browsing files: {str(e)}"
            self._update_group_status(error_msg)
            messagebox.showerror("Browse Error", error_msg)
    
    def handle_use_default_csv(self):
        """Handle use default group CSV files request"""
        try:
            # Look for CSV files in the groupCsvs directory
            csv_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'groupCsvs')
            
            if not os.path.exists(csv_dir):
                self._update_group_status("❌ Group CSV directory not found. Use 'Browse CSV Files' instead.")
                return
            
            csv_files = []
            for filename in os.listdir(csv_dir):
                if filename.endswith('.csv'):
                    csv_files.append(os.path.join(csv_dir, filename))
            
            if csv_files:
                self.selected_csv_files = csv_files
                file_names = [os.path.basename(f) for f in csv_files]
                self._update_group_status(f"📋 Using {len(csv_files)} group CSV files:\n" + 
                                        "\n".join([f"  • {name}" for name in file_names]) +
                                        "\n\nNow click a comparison button to generate plots.")
            else:
                self._update_group_status("❌ No CSV files found in group directory. Use 'Browse CSV Files' instead.")
                
        except Exception as e:
            error_msg = f"❌ Error loading group CSVs: {str(e)}"
            self._update_group_status(error_msg)
            messagebox.showerror("Group CSV Error", error_msg)
    
    def handle_auto_detect_csv(self):
        """Handle auto-detect CSV files request"""
        try:
            self._update_group_status("🔍 Auto-detecting CSV files...")
            
            # Use auto-detection to find all valid CSV files
            csv_files = self.auto_detect_csv_files()
            
            if csv_files:
                self.selected_csv_files = csv_files
                file_names = [os.path.basename(f) for f in csv_files]
                
                # Create detailed status message
                status_msg = f"🔍 Auto-detected {len(csv_files)} valid CSV files:\n"
                for file in csv_files:
                    directory = os.path.basename(os.path.dirname(file))
                    filename = os.path.basename(file)
                    status_msg += f"  • {filename} (from {directory})\n"
                
                status_msg += "\n✅ All files validated for weather data format"
                status_msg += "\n\nNow click a comparison button to generate plots."
                
                self._update_group_status(status_msg)
                
                print(f"✅ Auto-detected and selected {len(csv_files)} CSV files")
                
            else:
                error_msg = ("❌ No valid CSV files found with weather data format.\n\n"
                           "Expected format:\n"
                           "• Must have 'Temperature_F' column\n"  
                           "• Must have date/time columns (DateTime, Date+Time, or Date)\n"
                           "• Must contain numerical temperature data\n\n"
                           "Searched directories:\n"
                           "• data/groupCsvs/\n"
                           "• data/\n"
                           "• weather_data/\n"
                           "• csv_files/\n"
                           "• Root project directory")
                
                self._update_group_status(error_msg)
                messagebox.showwarning("No CSV Files Found", 
                                     "No valid weather CSV files found. Check the file format requirements.")
                
        except Exception as e:
            error_msg = f"❌ Error during auto-detection: {str(e)}"
            self._update_group_status(error_msg)
            messagebox.showerror("Auto-Detection Error", error_msg)
            print(f"Auto-detection error: {e}")
    
    def auto_detect_csv_files(self, directories=None):
        """
        Automatically detect CSV files in specified directories with weather data format validation
        
        Args:
            directories (list, optional): List of directories to search. If None, uses default directories.
            
        Returns:
            list: List of valid CSV file paths with weather data
        """
        if directories is None:
            # Default directories to search for CSV files
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            directories = [
                os.path.join(base_dir, 'data', 'groupCsvs'),
                os.path.join(base_dir, 'data'),
                os.path.join(base_dir, 'weather_data'),
                os.path.join(base_dir, 'csv_files'),
                base_dir  # Also check root directory
            ]
        
        csv_files = []
        
        for directory in directories:
            if not os.path.exists(directory):
                continue
                
            print(f"🔍 Scanning directory: {directory}")
            
            for filename in os.listdir(directory):
                if filename.endswith('.csv'):
                    filepath = os.path.join(directory, filename)
                    
                    # Validate CSV file format
                    if self._validate_csv_format(filepath):
                        csv_files.append(filepath)
                        print(f"✅ Found valid CSV: {filename}")
                    else:
                        print(f"⚠️ Skipped invalid CSV format: {filename}")
        
        # Sort files for consistent ordering
        csv_files.sort()
        
        print(f"📊 Auto-detected {len(csv_files)} valid CSV files")
        return csv_files
    
    def _validate_csv_format(self, filepath):
        """
        Validate that a CSV file has the expected weather data format
        
        Args:
            filepath (str): Path to the CSV file
            
        Returns:
            bool: True if the CSV has valid weather data format
        """
        try:
            import pandas as pd
            
            # Read just the first few rows to check format
            df = pd.read_csv(filepath, nrows=5)
            
            # Check for required columns
            required_columns = ['Temperature_F']
            has_temp_column = any(col in df.columns for col in required_columns)
            
            # Check for datetime columns (various formats supported)
            datetime_patterns = [
                'DateTime',
                ['Date', 'Time'],
                'Date',
                'Timestamp'
            ]
            
            has_datetime = False
            for pattern in datetime_patterns:
                if isinstance(pattern, list):
                    # Check if both Date and Time columns exist
                    if all(col in df.columns for col in pattern):
                        has_datetime = True
                        break
                else:
                    # Check if single datetime column exists
                    if pattern in df.columns:
                        has_datetime = True
                        break
            
            # Must have temperature data and some form of datetime
            is_valid = has_temp_column and has_datetime
            
            if is_valid and len(df) > 0:
                # Additional check: ensure we can read at least one temperature value
                try:
                    temp_col = next(col for col in required_columns if col in df.columns)
                    pd.to_numeric(df[temp_col].iloc[0])
                    return True
                except (ValueError, IndexError):
                    return False
            
            return is_valid
            
        except Exception as e:
            print(f"❌ Error validating {filepath}: {e}")
            return False
    
    def _get_csv_files(self):
        """Get the currently selected CSV files or auto-detect them"""
        # First, check if user has manually selected files
        if hasattr(self, 'selected_csv_files') and self.selected_csv_files:
            print("📁 Using manually selected CSV files")
            return self.selected_csv_files
        
        # If no manual selection, use auto-detection
        print("🔍 Auto-detecting CSV files...")
        csv_files = self.auto_detect_csv_files()
        
        if csv_files:
            print(f"✅ Auto-detected {len(csv_files)} CSV files:")
            for file in csv_files:
                print(f"  • {os.path.basename(file)}")
            return csv_files
        
        # Fallback: Try the old method for backwards compatibility
        print("⚠️ Auto-detection found no files, trying legacy method...")
        csv_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'groupCsvs')
        if os.path.exists(csv_dir):
            csv_files = []
            for filename in os.listdir(csv_dir):
                if filename.endswith('.csv'):
                    csv_files.append(os.path.join(csv_dir, filename))
            if csv_files:
                return csv_files
        
        print("❌ No CSV files found")
        return []
    
    def _update_group_status(self, message):
        """Update the group feature status text"""
        if 'group_textbox' in self.widgets:
            self.widgets['group_textbox'].delete("0.0", "end")
            self.widgets['group_textbox'].insert("0.0", message)
    
    def _save_weather_to_history(self, city, weather_data):
        """
        Save weather data to CSV history file
        """
        try:
            self.weather_history.add_weather_record(city, weather_data)
            # Update history display if it's currently showing recent history
            current_content = self.widgets['history_textbox'].get("0.0", "end")
            if "Recent Weather History" in current_content:
                self.handle_load_recent_history()
        except Exception as e:
            print(f"Failed to save to history: {e}")
