from tkinter import messagebox
from datetime import datetime
import requests
from core.weather_api import WeatherAPIError
from utils.state_validator import StateValidator


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
