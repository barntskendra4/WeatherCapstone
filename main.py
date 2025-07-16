import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import json
import os
import requests
from config import WEATHER_API_KEY, DEFAULT_CITY, WINDOW_WIDTH, WINDOW_HEIGHT, DEFAULT_THEME
from core.weather_api import WeatherAPI, WeatherAPIError
from features.city_comparison import CityComparison
from features.forecast_predict import ForecastPredict

# Set the appearance mode and color theme
ctk.set_appearance_mode("Light")  # Modes: "System", "Dark", "Light"
ctk.set_default_color_theme("data/red.json") #defaults are "blue", "green", "dark-blue"
class WeatherDashboard:
    """Main application controller with customTkinter GUI"""
    
    def __init__(self):
        try:
            self.api = WeatherAPI(WEATHER_API_KEY)
        except WeatherAPIError as e:
            # Show error message and exit gracefully
            messagebox.showerror("API Configuration Error", str(e))
            return
        
        self.root = ctk.CTk()
        self.city_comparison = CityComparison(self.api)
        self.forecast_predict = ForecastPredict(self.api)
        
        # Load user preferences
        self.preferences = self.load_preferences()
        
        # Setup GUI
        self.setup_window()
        self.create_widgets()
        self.apply_theme(self.preferences.get('theme', DEFAULT_THEME))
        
        # Load default city weather after GUI is ready
        self.root.after(100, lambda: self.get_weather(self.preferences.get('default_city', DEFAULT_CITY)))
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title("WeatherCap - Weather Dashboard")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(1000, 800)
        
        # # Center the window
        # self.center_window()
        
    # def center_window(self):
    #     """Center the window on the screen"""
    #     self.root.update_idletasks()
    #     width = self.root.winfo_width()
    #     height = self.root.winfo_height()
    #     x = (self.root.winfo_screenwidth() // 2) - (width // 2)
    #     y = (self.root.winfo_screenheight() // 2) - (height // 2)
    #     self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Create and layout all GUI widgets"""
        # Main container
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header frame with title and theme switcher
        header_frame = ctk.CTkFrame(self.main_frame)
        header_frame.pack(fill="x", pady=(10, 30))
        
        # Title on the left side
        title_label = ctk.CTkLabel(header_frame, text="WeatherCap Dashboard", 
                                  font=ctk.CTkFont(size=28, weight="bold"))
        title_label.pack(side="left", padx=(20, 0), pady=15)
        
        # Theme switcher on the right side
        theme_frame = ctk.CTkFrame(header_frame)
        theme_frame.pack(side="right", padx=(0, 20), pady=15)
        
        # Dark mode toggle
        ctk.CTkLabel(theme_frame, text="Dark Mode:", 
                    font=ctk.CTkFont(size=12, weight="bold")).pack(side="left", padx=(10, 8))
        
        # Create theme toggle switch
        self.theme_switch = ctk.CTkSwitch(theme_frame, text="", width=50, height=24,
                                         command=self.on_theme_toggle)
        
        # Set initial state based on preferences
        if self.preferences.get('theme', 'light') == 'dark':
            self.theme_switch.select()
        else:
            self.theme_switch.deselect()
            
        self.theme_switch.pack(side="left", padx=(0, 10))
        
        # Search frame
        self.create_search_frame()
        
        # Main content container for side-by-side layout
        self.create_main_content()
        
        # Settings frame (without theme switcher now)
        self.create_settings_frame()
        
        # Status bar
        self.create_status_bar()
    
    
    def create_search_frame(self):
        """Create the city search interface"""
        search_frame = ctk.CTkFrame(self.main_frame)
        search_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        # Title
        search_title = ctk.CTkLabel(search_frame, text="Search Weather", 
                                   font=ctk.CTkFont(size=16, weight="bold"))
        search_title.pack(pady=(15, 10))
        
        # Search container
        search_container = ctk.CTkFrame(search_frame)
        search_container.pack(fill="x", padx=20, pady=(0, 15))
        
        # City label and entry
        ctk.CTkLabel(search_container, text="City:", 
                    font=ctk.CTkFont(size=14)).pack(side="left", padx=(10, 5))
        
        self.city_entry = ctk.CTkEntry(search_container, placeholder_text="Enter city name...", 
                                      width=300, font=ctk.CTkFont(size=14))
        self.city_entry.pack(side="left", padx=(0, 10), pady=10)
        self.city_entry.insert(0, self.preferences.get('default_city', DEFAULT_CITY))
        self.city_entry.bind('<Return>', lambda e: self.search_weather())
        
        self.search_btn = ctk.CTkButton(search_container, text="Get Weather", 
                                       command=self.search_weather, width=120,
                                       font=ctk.CTkFont(size=14, weight="bold"))
        self.search_btn.pack(side="left", padx=(0, 10), pady=10)
    
    def create_main_content(self):
        """Create the main content area with side-by-side layout"""
        # Main content container
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 20))
        
        # Left side - Current weather display
        self.create_weather_display()
        
        # Right side - Features tabs
        self.create_features_tabs()
    
    def create_weather_display(self):
        """Create the main weather information display"""
        self.weather_frame = ctk.CTkFrame(self.content_frame)
        self.weather_frame.pack(side="left", fill="y", expand=False, padx=(10, 10), pady=10)
        self.weather_frame.configure(width=380)  # Fixed width for weather display
        
        # Title
        weather_title = ctk.CTkLabel(self.weather_frame, text="Current Weather", 
                                    font=ctk.CTkFont(size=16, weight="bold"))
        weather_title.pack(pady=(15, 5))
        
        # City name
        self.city_label = ctk.CTkLabel(self.weather_frame, text="Select a city", 
                                      font=ctk.CTkFont(size=20, weight="bold"))
        self.city_label.pack(pady=(5, 10))
        
        # Temperature display container
        temp_container = ctk.CTkFrame(self.weather_frame, corner_radius=50)
        temp_container.pack(pady=10)
        
        # Temperature
        self.temp_label = ctk.CTkLabel(temp_container, text="--°F", 
                                      font=ctk.CTkFont(size=48, weight="bold"),
                                      text_color="#000000")
        self.temp_label.pack(padx=30, pady=20)
        
        # Description
        self.desc_label = ctk.CTkLabel(self.weather_frame, text="--", 
                                      font=ctk.CTkFont(size=16))
        self.desc_label.pack(pady=(0, 10))
        
        # Additional info container
        info_container = ctk.CTkFrame(self.weather_frame)
        info_container.pack(pady=(0, 15))
        
        # Info grid
        info_grid = ctk.CTkFrame(info_container)
        info_grid.pack(padx=20, pady=15)
        
        # Humidity
        humidity_frame = ctk.CTkFrame(info_grid)
        humidity_frame.pack(side="left", padx=10)
        
        ctk.CTkLabel(humidity_frame, text="Humidity", 
                    font=ctk.CTkFont(size=12, weight="bold"), text_color="#5400D2").pack(pady=(10, 5))
        self.humidity_label = ctk.CTkLabel(humidity_frame, text="--%", 
                                          font=ctk.CTkFont(size=14))
        self.humidity_label.pack(pady=(0, 10))
        
        # Last updated
        updated_frame = ctk.CTkFrame(info_grid)
        updated_frame.pack(side="left", padx=10)
        
        ctk.CTkLabel(updated_frame, text="Updated", 
                    font=ctk.CTkFont(size=12, weight="bold"), text_color="#5400D2").pack(pady=(10, 5))
        self.updated_label = ctk.CTkLabel(updated_frame, text="--", 
                                         font=ctk.CTkFont(size=14))
        self.updated_label.pack(pady=(0, 10))
    
    def create_features_tabs(self):
        """Create the features tabview"""
        self.tabview = ctk.CTkTabview(self.content_frame, width=520, height=420)
        self.tabview.pack(side="right", fill="both", expand=True, padx=(0, 10), pady=10)
        
        # City Comparison Tab
        self.tabview.add("City Comparison")
        self.create_city_comparison_tab(self.tabview.tab("City Comparison"))
        
        # Weather Forecast Tab
        self.tabview.add("Weather Forecast")
        self.create_forecast_tab(self.tabview.tab("Weather Forecast"))
        
        # History Tab
        self.tabview.add("Weather History")
        self.create_history_tab(self.tabview.tab("Weather History"))
        
        # Settings Tab
        self.tabview.add("Settings & Preferences")
        self.create_settings_tab(self.tabview.tab("Settings & Preferences"))
    
    def create_city_comparison_tab(self, parent):
        """Create the city comparison interface"""
        comparison_frame = ctk.CTkFrame(parent)
        comparison_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(comparison_frame, text="City Weather Comparison", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(5, 5))
        
        # Input section
        input_frame = ctk.CTkFrame(comparison_frame)
        input_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Input container for side-by-side layout
        input_container = ctk.CTkFrame(input_frame)
        input_container.pack(pady=20)
        
        # City 1 input
        city1_frame = ctk.CTkFrame(input_container)
        city1_frame.pack(side="left", padx=(20, 10))
        
        ctk.CTkLabel(city1_frame, text="City 1:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
        self.city1_entry = ctk.CTkEntry(city1_frame, placeholder_text="Enter first city...", 
                                       width=200, font=ctk.CTkFont(size=14))
        self.city1_entry.pack(padx=15, pady=(0, 15))
        self.city1_entry.bind('<Return>', lambda e: self.compare_cities())
        
        # VS separator
        vs_frame = ctk.CTkFrame(input_container)
        vs_frame.pack(side="left", padx=10)
        
        ctk.CTkLabel(vs_frame, text="VS", 
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color="#5400D2").pack(padx=20, pady=35)
        
        # City 2 input
        city2_frame = ctk.CTkFrame(input_container)
        city2_frame.pack(side="left", padx=(10, 20))
        
        ctk.CTkLabel(city2_frame, text="City 2:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
        self.city2_entry = ctk.CTkEntry(city2_frame, placeholder_text="Enter second city...", 
                                       width=200, font=ctk.CTkFont(size=14))
        self.city2_entry.pack(padx=15, pady=(0, 15))
        self.city2_entry.bind('<Return>', lambda e: self.compare_cities())
        
        # Compare button
        compare_btn = ctk.CTkButton(comparison_frame, text="🔄 Compare Cities", 
                                   command=self.compare_cities, width=200, height=40,
                                   font=ctk.CTkFont(size=16, weight="bold"))
        compare_btn.pack(pady=(0, 20))
        
        # Results section
        results_frame = ctk.CTkFrame(comparison_frame)
        results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(results_frame, text="Comparison Results", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))
        
        # Results display
        self.comparison_textbox = ctk.CTkTextbox(results_frame, font=ctk.CTkFont(size=12))
        self.comparison_textbox.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.comparison_textbox.insert("0.0", "Enter two cities above and click 'Compare Cities' to see detailed weather comparison.")
    
    def create_history_tab(self, parent):
        """Create the weather history interface"""
        history_frame = ctk.CTkFrame(parent)
        history_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(history_frame, text="Weather History", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 10))
        
        # History display
        self.history_textbox = ctk.CTkTextbox(history_frame, font=ctk.CTkFont(size=12))
        self.history_textbox.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Load and display history
        self.load_weather_history()
    
    def create_forecast_tab(self, parent):
        """Create the weather forecast interface"""
        forecast_frame = ctk.CTkFrame(parent)
        forecast_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(forecast_frame, text="Weather Forecast", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 15))
        
        # Input section
        input_frame = ctk.CTkFrame(forecast_frame)
        input_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        input_container = ctk.CTkFrame(input_frame)
        input_container.pack(pady=15)
        
        # City input
        ctk.CTkLabel(input_container, text="City:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=(20, 10))
        
        self.forecast_city_entry = ctk.CTkEntry(input_container, placeholder_text="Enter city name...", 
                                              width=200, font=ctk.CTkFont(size=14))
        self.forecast_city_entry.pack(side="left", padx=(0, 15))
        self.forecast_city_entry.bind('<Return>', lambda e: self.get_forecast())
        
        # Buttons container
        button_frame = ctk.CTkFrame(input_container)
        button_frame.pack(side="left", padx=(15, 20))
        
        # 5-day forecast button
        forecast_btn = ctk.CTkButton(button_frame, text="📅 5-Day Forecast", 
                                   command=self.get_forecast, width=140, height=32,
                                   font=ctk.CTkFont(size=13, weight="bold"))
        forecast_btn.pack(side="left", padx=(0, 10))
        
        # Weather trends button
        trends_btn = ctk.CTkButton(button_frame, text="📈 Weather Trends", 
                                 command=self.get_weather_trends, width=140, height=32,
                                 font=ctk.CTkFont(size=13, weight="bold"))
        trends_btn.pack(side="left")
        
        # Results section
        results_frame = ctk.CTkFrame(forecast_frame)
        results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(results_frame, text="Forecast Results", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))
        
        # Results display
        self.forecast_textbox = ctk.CTkTextbox(results_frame, font=ctk.CTkFont(size=11))
        self.forecast_textbox.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.forecast_textbox.insert("0.0", "Enter a city name above and click '5-Day Forecast' to see detailed weather predictions, or click 'Weather Trends' for analysis.")
    
    
    def create_settings_tab(self, parent):
        """Create the settings interface as a tab"""
        settings_frame = ctk.CTkFrame(parent)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Settings title
        ctk.CTkLabel(settings_frame, text="Settings & Preferences", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(20, 15))
        
        # Settings content
        content_frame = ctk.CTkFrame(settings_frame)
        content_frame.pack(fill="x", padx=20, pady=10)
        
        # Save preferences section
        save_section = ctk.CTkFrame(content_frame)
        save_section.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(save_section, text="Save Your Preferences", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))
        
        ctk.CTkLabel(save_section, text="Click below to save your current theme and default city settings.",
                    font=ctk.CTkFont(size=12)).pack(pady=(0, 10))
        
        save_btn = ctk.CTkButton(save_section, text="💾 Save Settings", 
                                command=self.save_preferences, width=180, height=36,
                                font=ctk.CTkFont(size=14, weight="bold"))
        save_btn.pack(pady=(10, 20))
        
        # Info section
        info_frame = ctk.CTkFrame(settings_frame)
        info_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(info_frame, text="Application Info", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))
        
        info_text = ctk.CTkTextbox(info_frame, height=100)
        info_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        info_text.insert("0.0", "WeatherCap Dashboard v1.0\n\n• Real-time weather data\n• City comparison features\n• Dark/Light theme support\n• Weather history tracking\n• User preference persistence")
    
    def create_settings_frame(self):
        """Create minimal settings frame (most moved to tab)"""
        pass  # Settings moved to tab, keeping method for compatibility
    
    def create_status_bar(self):
        """Create the status bar"""
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        self.status_label = ctk.CTkLabel(self.status_frame, text="Ready", 
                                        font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=8, padx=15, anchor="w")
    
    def search_weather(self):
        """Search for weather information"""
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name")
            return
        
        self.get_weather(city)
    
    def get_weather(self, city):
        """Get weather information for a city"""
        try:
            self.status_label.configure(text=f"Getting weather for {city}...")
            self.root.update()
            
            weather_data = self.api.get_weather_from_api(city)
            
            # Update display
            self.city_label.configure(text=city.title())
            self.temp_label.configure(text=f"{weather_data['temperature']:.0f}°F")
            self.desc_label.configure(text=weather_data['description'].title())
            self.humidity_label.configure(text=f"{weather_data['humidity']}%")
            self.updated_label.configure(text=datetime.now().strftime("%I:%M %p"))
            
            # Save to history
            self.save_weather_to_history(city, weather_data)
            
            self.status_label.configure(text=f"Weather updated for {city}")
            
        except KeyError as e:
            messagebox.showerror("Error", str(e))
            self.status_label.configure(text="City not found")
        except WeatherAPIError as e:
            messagebox.showerror("API Error", str(e))
            self.status_label.configure(text="API error")
        except ValueError as e:
            messagebox.showerror("Configuration Error", str(e))
            self.status_label.configure(text="Configuration error")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Network Error", f"Network error: {str(e)}")
            self.status_label.configure(text="Network error")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            self.status_label.configure(text="Unexpected error")
    
    def compare_cities(self):
        """Compare weather between two cities"""
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        
        if not city1 or not city2:
            messagebox.showwarning("Warning", "Please enter both city names")
            return
        
        try:
            self.status_label.configure(text="Comparing cities...")
            comparison_result = self.city_comparison.compare_cities(city1, city2)
            
            self.comparison_textbox.delete("0.0", "end")
            self.comparison_textbox.insert("0.0", comparison_result)
            
            self.status_label.configure(text=f"Compared {city1} and {city2}")
            
        except KeyError as e:
            messagebox.showerror("Error", str(e))
            self.status_label.configure(text="City not found")
        except WeatherAPIError as e:
            messagebox.showerror("API Error", str(e))
            self.status_label.configure(text="API error")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to compare cities: {str(e)}")
            self.status_label.configure(text="Error comparing cities")
    
    def get_forecast(self):
        """Get 5-day weather forecast for a city"""
        city = self.forecast_city_entry.get().strip()
        
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name")
            return
        
        try:
            self.status_label.configure(text=f"Getting 5-day forecast for {city}...")
            self.root.update()
            
            forecast_result = self.forecast_predict.get_5_day_forecast(city)
            
            self.forecast_textbox.delete("0.0", "end")
            self.forecast_textbox.insert("0.0", forecast_result)
            
            self.status_label.configure(text=f"5-day forecast for {city}")
            
        except WeatherAPIError as e:
            messagebox.showerror("API Error", str(e))
            self.status_label.configure(text="API error")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get forecast: {str(e)}")
            self.status_label.configure(text="Error getting forecast")
    
    def get_weather_trends(self):
        """Get weather trends and analysis for a city"""
        city = self.forecast_city_entry.get().strip()
        
        if not city:
            messagebox.showwarning("Warning", "Please enter a city name")
            return
        
        try:
            self.status_label.configure(text=f"Analyzing weather trends for {city}...")
            self.root.update()
            
            trends_result = self.forecast_predict.analyze_weather_trends(city)
            
            self.forecast_textbox.delete("0.0", "end")
            self.forecast_textbox.insert("0.0", trends_result)
            
            self.status_label.configure(text=f"Weather trends analyzed for {city}")
            
        except WeatherAPIError as e:
            messagebox.showerror("API Error", str(e))
            self.status_label.configure(text="API error")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze trends: {str(e)}")
            self.status_label.configure(text="Error analyzing trends")
    
    
    def on_theme_toggle(self):
        """Handle theme toggle switch change"""
        if self.theme_switch.get():
            self.apply_theme("dark")
        else:
            self.apply_theme("light")
    
    # def on_theme_change(self, theme):
    #     """Handle theme change (kept for compatibility)"""
    #     self.apply_theme(theme)
    
    def apply_theme(self, theme):
        """Apply the selected theme (simplified - only light/dark)"""
        if theme == "dark":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
        # Update preferences
        self.preferences['theme'] = theme
    
    def save_weather_to_history(self, city, weather_data):
        """Save weather data to history file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry = f"{timestamp} - {city}: {weather_data['temperature']:.0f}°F, {weather_data['description']}, Humidity: {weather_data['humidity']}%\n"
        
        history_file = "data/weather_history.txt"
        try:
            os.makedirs(os.path.dirname(history_file), exist_ok=True)
            with open(history_file, "a", encoding="utf-8") as f:
                f.write(history_entry)
            # Update history display
            self.load_weather_history()
        except Exception as e:
            print(f"Failed to save to history: {e}")
    
    def load_weather_history(self):
        """Load and display weather history"""
        history_file = "data/weather_history.txt"
        try:
            if os.path.exists(history_file):
                with open(history_file, "r", encoding="utf-8") as f:
                    history = f.read()
                    # Show only the last 20 entries
                    lines = history.strip().split('\n')
                    recent_history = '\n'.join(lines[-20:]) if lines else "No history available"
                    self.history_textbox.delete("0.0", "end")
                    self.history_textbox.insert("0.0", recent_history)
            else:
                self.history_textbox.delete("0.0", "end")
                self.history_textbox.insert("0.0", "No history available")
        except Exception as e:
            self.history_textbox.delete("0.0", "end")
            self.history_textbox.insert("0.0", f"Error loading history: {e}")
    
    def load_preferences(self):
        """Load user preferences from file"""
        prefs_file = "data/user_preferences.json"
        default_prefs = {
            'theme': DEFAULT_THEME,
            'default_city': DEFAULT_CITY
        }
        
        try:
            if os.path.exists(prefs_file):
                with open(prefs_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                return default_prefs
        except Exception:
            return default_prefs
    
    def save_preferences(self):
        """Save user preferences to file"""
        prefs = {
            'theme': 'dark' if self.theme_switch.get() else 'light',
            'default_city': self.city_entry.get()
        }
        
        prefs_file = "data/user_preferences.json"
        try:
            os.makedirs(os.path.dirname(prefs_file), exist_ok=True)
            with open(prefs_file, "w", encoding="utf-8") as f:
                json.dump(prefs, f, indent=2)
            
            messagebox.showinfo("Settings", "Preferences saved successfully!")
            self.status_label.configure(text="Preferences saved")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save preferences: {e}")
            self.status_label.configure(text="Error saving preferences")
    
    def run(self):
        """Start the application"""
        # Check if initialization was successful (API key validation)
        if hasattr(self, 'root') and self.root:
            self.root.mainloop()
        else:
            # API initialization failed, don't start the app
            print("Application failed to initialize due to API configuration error.")

if __name__ == "__main__":
    try:
        weather_app = WeatherDashboard()
        weather_app.run()
    except WeatherAPIError as e:
        print(f"Failed to start application: {e}")
    except Exception as e:
        print(f"Unexpected error starting application: {e}")
