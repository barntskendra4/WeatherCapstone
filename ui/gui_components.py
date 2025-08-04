"""
GUI Components Module - Contains all UI widget creation and layout logic
Separates UI construction from business logic and event handling
"""

import customtkinter as ctk
from datetime import datetime


class WeatherGUIComponents:
    """Handles all GUI widget creation and layout"""
    
    def __init__(self, root, preferences):
        """
        Initialize GUI components
        
        Args:
            root: The main CTk root window
            preferences (dict): User preferences        #         initial_message = ("🌤️ Temperature Comparison Tools\n\n"
                          "📊 CSV Comparison Only: Compare historical temperature data from multiple CSV files\n"
                          "🌐 CSV + Recent Temps: Combine historical data with recent temperature trends\n\n"
                          "Instructions:\n"
                          "1. Enter cities for temperature data (optional)\n"
                          "2. Choose CSV files or use default group CSVs\n"
                          "3. Click a comparison button to generate graphs\n\n"
                          "Supported CSV format: Date, Time, City, Temperature_F\n"
                          "Generated plots will be saved in the WeatherCap directory.")ssage
        initial_message = ("🌤️ Temperature Comparison Tools\n\n"
                          "📊 CSV Comparison Only: Compare historical temperature data from multiple CSV files\n"
                          "🌐 CSV + Recent Temps: Combine historical data with recent temperature trends\n\n"
                          "Instructions:\n"
                          "1. Enter cities for temperature data (optional)\n"
                          "2. Choose CSV files or use default group CSVs\n"
                          "3. Click a comparison button to generate graphs\n\n"
                          "Supported CSV format: Date, Time, City, Temperature_F\n"
                          "Generated plots will be saved in the WeatherCap directory.")itial_message = ("�️ Temperature Comparison Tools\n\n"
                          "📊 CSV Comparison Only: Compare historical temperature data from multiple CSV files\n"
                          "�️ CSV + Recent Temps: Combine historical data with recent temperature trends\n"
                          "🎬 Run Demo: See a demonstration with sample data\n\n"
                          "Instructions:\n"
                          "1. Enter cities for temperature data (optional)\n"
                          "2. Choose CSV files or use default group CSVs\n"
                          "3. Click a comparison button to generate graphs\n\n"
                          "Supported CSV format: Date, Time, City, Temperature_F\n"
                          "Generated plots will be saved in the WeatherCap directory.")t values
        """
        self.root = root
        self.preferences = preferences
        self.widgets = {}  # Store widget references
        
    def setup_main_layout(self):
        """Create the main application layout structure"""
        # Main container
        self.widgets['main_frame'] = ctk.CTkFrame(self.root)
        self.widgets['main_frame'].pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create all major sections
        self._create_header_frame()
        self._create_search_frame()
        self._create_main_content()
        self._create_status_bar()
        
        return self.widgets
    
    def _create_header_frame(self):
        """Create the header with title and theme controls"""
        header_frame = ctk.CTkFrame(self.widgets['main_frame'])
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
        self.widgets['theme_switch'] = ctk.CTkSwitch(theme_frame, text="", width=50, height=24)
        
        # Set initial state based on preferences
        if self.preferences.get('theme', 'light') == 'dark':
            self.widgets['theme_switch'].select()
        else:
            self.widgets['theme_switch'].deselect()
            
        self.widgets['theme_switch'].pack(side="left", padx=(0, 10))
    
    def _create_search_frame(self):
        """Create the city and state search interface"""
        search_frame = ctk.CTkFrame(self.widgets['main_frame'])
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
        
        self.widgets['city_entry'] = ctk.CTkEntry(search_container, placeholder_text="Enter city name...", 
                                      width=250, font=ctk.CTkFont(size=14))
        self.widgets['city_entry'].pack(side="left", padx=(0, 10), pady=10)
        self.widgets['city_entry'].insert(0, self.preferences.get('default_city', 'Miami'))
        
        # State label and entry (optional)
        ctk.CTkLabel(search_container, text="State:", 
                    font=ctk.CTkFont(size=14)).pack(side="left", padx=(5, 5))
        
        self.widgets['state_entry'] = ctk.CTkEntry(search_container, placeholder_text="Optional (FL, TX, California, etc.)", 
                                       width=200, font=ctk.CTkFont(size=14))
        self.widgets['state_entry'].pack(side="left", padx=(0, 10), pady=10)
        
        self.widgets['search_btn'] = ctk.CTkButton(search_container, text="Get Weather", 
                                       width=120, font=ctk.CTkFont(size=14, weight="bold"))
        self.widgets['search_btn'].pack(side="left", padx=(0, 10), pady=10)
    
    def _create_main_content(self):
        """Create the main content area with side-by-side layout"""
        # Main content container
        self.widgets['content_frame'] = ctk.CTkFrame(self.widgets['main_frame'])
        self.widgets['content_frame'].pack(fill="both", expand=True, padx=10, pady=(0, 20))
        
        # Left side - Current weather display
        self._create_weather_display()
        
        # Right side - Features tabs
        self._create_features_tabs()
    
    def _create_weather_display(self):
        """Create the main weather information display"""
        self.widgets['weather_frame'] = ctk.CTkFrame(self.widgets['content_frame'])
        self.widgets['weather_frame'].pack(side="left", fill="y", expand=False, padx=(10, 10), pady=10)
        self.widgets['weather_frame'].configure(width=380)  # Fixed width for weather display
        
        # Title
        weather_title = ctk.CTkLabel(self.widgets['weather_frame'], text="Current Weather", 
                                    font=ctk.CTkFont(size=16, weight="bold"))
        weather_title.pack(pady=(15, 5))
        
        # City name
        self.widgets['city_label'] = ctk.CTkLabel(self.widgets['weather_frame'], text="Select a city", 
                                      font=ctk.CTkFont(size=20, weight="bold"))
        self.widgets['city_label'].pack(pady=(5, 10))
        
        # Temperature display container
        temp_container = ctk.CTkFrame(self.widgets['weather_frame'], corner_radius=50)
        temp_container.pack(pady=10)
        
        # Temperature
        self.widgets['temp_label'] = ctk.CTkLabel(temp_container, text="--°F", 
                                      font=ctk.CTkFont(size=48, weight="bold"),
                                      text_color="#000000")
        self.widgets['temp_label'].pack(padx=30, pady=20)
        
        # Description
        self.widgets['desc_label'] = ctk.CTkLabel(self.widgets['weather_frame'], text="--", 
                                      font=ctk.CTkFont(size=16))
        self.widgets['desc_label'].pack(pady=(0, 10))
        
        # Additional info container
        info_container = ctk.CTkFrame(self.widgets['weather_frame'])
        info_container.pack(pady=(0, 15))
        
        # Info grid
        info_grid = ctk.CTkFrame(info_container)
        info_grid.pack(padx=20, pady=15)
        
        # Humidity
        humidity_frame = ctk.CTkFrame(info_grid)
        humidity_frame.pack(side="left", padx=10)
        
        ctk.CTkLabel(humidity_frame, text="Humidity", 
                    font=ctk.CTkFont(size=12, weight="bold"), text_color="#5400D2").pack(pady=(10, 5))
        self.widgets['humidity_label'] = ctk.CTkLabel(humidity_frame, text="--%", 
                                          font=ctk.CTkFont(size=14))
        self.widgets['humidity_label'].pack(pady=(0, 10))
        
        # Last updated
        updated_frame = ctk.CTkFrame(info_grid)
        updated_frame.pack(side="left", padx=10)
        
        ctk.CTkLabel(updated_frame, text="Updated", 
                    font=ctk.CTkFont(size=12, weight="bold"), text_color="#5400D2").pack(pady=(10, 5))
        self.widgets['updated_label'] = ctk.CTkLabel(updated_frame, text="--", 
                                         font=ctk.CTkFont(size=14))
        self.widgets['updated_label'].pack(pady=(0, 10))
    
    def _create_features_tabs(self):
        """Create the features tabview"""
        self.widgets['tabview'] = ctk.CTkTabview(self.widgets['content_frame'], width=520, height=420)
        self.widgets['tabview'].pack(side="right", fill="both", expand=True, padx=(0, 10), pady=10)
        
        # Create tabs
        self.widgets['tabview'].add("City Comparison")
        self.widgets['tabview'].add("Weather Forecast")
        self.widgets['tabview'].add("Weather History")
        self.widgets['tabview'].add("Group Feature")
        self.widgets['tabview'].add("Settings & Preferences")
        
        # Create tab contents
        self._create_city_comparison_tab()
        self._create_forecast_tab()
        self._create_history_tab()
        self._create_group_feature_tab()
        self._create_settings_tab()
    
    def _create_city_comparison_tab(self):
        """Create the city comparison interface"""
        parent = self.widgets['tabview'].tab("City Comparison")
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
        self.widgets['city1_entry'] = ctk.CTkEntry(city1_frame, placeholder_text="Enter first city...", 
                                       width=150, font=ctk.CTkFont(size=12))
        self.widgets['city1_entry'].pack(padx=15, pady=(0, 5))
        
        ctk.CTkLabel(city1_frame, text="State (optional):", 
                    font=ctk.CTkFont(size=12)).pack(pady=(5, 2))
        self.widgets['state1_entry'] = ctk.CTkEntry(city1_frame, placeholder_text="FL, California, etc.", 
                                        width=150, font=ctk.CTkFont(size=12))
        self.widgets['state1_entry'].pack(padx=15, pady=(0, 15))
        
        # VS separator with compare button
        vs_frame = ctk.CTkFrame(input_container)
        vs_frame.pack(side="left", padx=10)
        
        ctk.CTkLabel(vs_frame, text="VS", 
                    font=ctk.CTkFont(size=20, weight="bold"),
                    text_color="#5400D2").pack(padx=20, pady=(30, 10))
        
        # Compare button in the VS section
        self.widgets['compare_btn'] = ctk.CTkButton(vs_frame, text="🔄 Compare", 
                                   width=140, height=36, font=ctk.CTkFont(size=14, weight="bold"))
        self.widgets['compare_btn'].pack(padx=20, pady=(10, 30))
        
        # City 2 input
        city2_frame = ctk.CTkFrame(input_container)
        city2_frame.pack(side="left", padx=(10, 20))
        
        ctk.CTkLabel(city2_frame, text="City 2:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
        self.widgets['city2_entry'] = ctk.CTkEntry(city2_frame, placeholder_text="Enter second city...", 
                                       width=150, font=ctk.CTkFont(size=12))
        self.widgets['city2_entry'].pack(padx=15, pady=(0, 5))
        
        ctk.CTkLabel(city2_frame, text="State (optional):", 
                    font=ctk.CTkFont(size=12)).pack(pady=(5, 2))
        self.widgets['state2_entry'] = ctk.CTkEntry(city2_frame, placeholder_text="TX, New York, etc.", 
                                        width=150, font=ctk.CTkFont(size=12))
        self.widgets['state2_entry'].pack(padx=15, pady=(0, 15))
        
        # Results section
        results_frame = ctk.CTkFrame(comparison_frame)
        results_frame.pack(fill="both", expand=True, padx=20, pady=(5, 5))
        
        ctk.CTkLabel(results_frame, text="Comparison Results", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))
        
        # Results display
        self.widgets['comparison_textbox'] = ctk.CTkTextbox(results_frame, font=ctk.CTkFont(size=12))
        self.widgets['comparison_textbox'].pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.widgets['comparison_textbox'].insert("0.0", "Enter two cities above and click 'Compare Cities' to see detailed weather comparison.")
    
    def _create_forecast_tab(self):
        """Create the weather forecast interface"""
        parent = self.widgets['tabview'].tab("Weather Forecast")
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
        
        self.widgets['forecast_city_entry'] = ctk.CTkEntry(input_container, placeholder_text="Enter city name...", 
                                              width=200, font=ctk.CTkFont(size=14))
        self.widgets['forecast_city_entry'].pack(side="left", padx=(0, 10))
        
        # State input (optional)
        ctk.CTkLabel(input_container, text="State:", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(side="left", padx=(10, 5))
        
        self.widgets['forecast_state_entry'] = ctk.CTkEntry(input_container, placeholder_text="Optional (CA, Texas, FL, etc.)", 
                                               width=150, font=ctk.CTkFont(size=14))
        self.widgets['forecast_state_entry'].pack(side="left", padx=(0, 15))
        
        # Buttons container
        button_frame = ctk.CTkFrame(input_container)
        button_frame.pack(side="left", padx=(15, 20))
        
        # Forecast buttons
        self.widgets['forecast_btn'] = ctk.CTkButton(button_frame, text="📅 5-Day Forecast", 
                                   width=140, height=32, font=ctk.CTkFont(size=13, weight="bold"))
        self.widgets['forecast_btn'].pack(side="left")
        
        # Results section
        results_frame = ctk.CTkFrame(forecast_frame)
        results_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(results_frame, text="Forecast Results", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))
        
        # Results display
        self.widgets['forecast_textbox'] = ctk.CTkTextbox(results_frame, font=ctk.CTkFont(size=11))
        self.widgets['forecast_textbox'].pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.widgets['forecast_textbox'].insert("0.0", "Enter a city name (and optional state) above and click:\n• '5-Day Forecast' for detailed weather predictions\n• 'Weather Trends' for analysis\n• 'Accuracy Report' to see how accurate our past forecasts were\n\nTip: Add state (e.g., CA, TX) to distinguish between cities with the same name")
    
    def _create_history_tab(self):
        """Create the weather history interface"""
        parent = self.widgets['tabview'].tab("Weather History")
        history_frame = ctk.CTkFrame(parent)
        history_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header with title and controls
        header_frame = ctk.CTkFrame(history_frame)
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(header_frame, text="Weather History", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(side="left", pady=10)
        
        # Buttons for different views
        button_frame = ctk.CTkFrame(header_frame)
        button_frame.pack(side="right", pady=10)
        
        self.widgets['recent_btn'] = ctk.CTkButton(button_frame, text="📈 Recent", 
                                  width=100, height=32, font=ctk.CTkFont(size=12, weight="bold"))
        self.widgets['recent_btn'].pack(side="left", padx=(0, 10))
        
        self.widgets['stats_btn'] = ctk.CTkButton(button_frame, text="📊 Statistics", 
                                 width=100, height=32, font=ctk.CTkFont(size=12, weight="bold"))
        self.widgets['stats_btn'].pack(side="left")
        
        # History display
        self.widgets['history_textbox'] = ctk.CTkTextbox(history_frame, font=ctk.CTkFont(size=12))
        self.widgets['history_textbox'].pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def _create_settings_tab(self):
        """Create the settings interface"""
        parent = self.widgets['tabview'].tab("Settings & Preferences")
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
        
        self.widgets['save_btn'] = ctk.CTkButton(save_section, text="💾 Save Settings", 
                                width=180, height=36, font=ctk.CTkFont(size=14, weight="bold"))
        self.widgets['save_btn'].pack(pady=(10, 20))
        
        # Info section
        info_frame = ctk.CTkFrame(settings_frame)
        info_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(info_frame, text="Application Info", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))
        
        info_text = ctk.CTkTextbox(info_frame, height=100)
        info_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        info_text.insert("0.0", "WeatherCap Dashboard v1.0\n\n• Real-time weather data\n• City comparison features\n• Dark/Light theme support\n• Weather history tracking\n• User preference persistence")
    
    def _create_status_bar(self):
        """Create the status bar"""
        self.widgets['status_frame'] = ctk.CTkFrame(self.widgets['main_frame'])
        self.widgets['status_frame'].pack(fill="x", padx=10, pady=(10, 0))
        
        self.widgets['status_label'] = ctk.CTkLabel(self.widgets['status_frame'], text="Ready", 
                                        font=ctk.CTkFont(size=12))
        self.widgets['status_label'].pack(pady=8, padx=15, anchor="w")
    
    def _create_group_feature_tab(self):
        """Create the group collaboration feature interface with CSV comparison and live weather data"""
        parent = self.widgets['tabview'].tab("Group Feature")
        group_frame = ctk.CTkFrame(parent)
        group_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        ctk.CTkLabel(group_frame, text="Temperature Comparison", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(10, 15))
        
        # Description
        description_frame = ctk.CTkFrame(group_frame)
        description_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        description_text = ("Compare historical CSV temperature data with recent temperature trends!\n"
                          "Load multiple CSV files and compare with recent temperature data.")
        ctk.CTkLabel(description_frame, text=description_text, 
                    font=ctk.CTkFont(size=12), wraplength=450).pack(pady=15, padx=20)
        
        # Main control section
        control_section = ctk.CTkFrame(group_frame)
        control_section.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(control_section, text="Temperature Data Comparison", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))
        
        # Control buttons frame
        buttons_frame = ctk.CTkFrame(control_section)
        buttons_frame.pack(pady=(0, 15))
        
        # CSV Comparison button
        self.widgets['csv_comparison_btn'] = ctk.CTkButton(
            buttons_frame, 
            text="� CSV Comparison Only", 
            width=160, height=36, 
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.widgets['csv_comparison_btn'].pack(side="left", padx=(20, 10), pady=10)
        
        # Live + CSV Comparison button
        self.widgets['live_csv_comparison_btn'] = ctk.CTkButton(
            buttons_frame, 
            text="�️ CSV + Recent Temps", 
            width=180, height=36, 
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.widgets['live_csv_comparison_btn'].pack(side="left", padx=(0, 20), pady=10)
        
        # Live cities configuration section
        config_section = ctk.CTkFrame(group_frame)
        config_section.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(config_section, text="Temperature Cities", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))
        
        # Cities input
        cities_input_frame = ctk.CTkFrame(config_section)
        cities_input_frame.pack(pady=(0, 15))
        
        ctk.CTkLabel(cities_input_frame, text="Cities for temperature data (comma-separated):", 
                    font=ctk.CTkFont(size=12)).pack(pady=(10, 5))
        
        self.widgets['live_cities_entry'] = ctk.CTkEntry(
            cities_input_frame, 
            placeholder_text="Toronto, Lincoln, Rockland, Los Angeles", 
            width=400, 
            font=ctk.CTkFont(size=12)
        )
        self.widgets['live_cities_entry'].pack(padx=20, pady=(0, 5))
        
        # Add note about zip codes
        ctk.CTkLabel(cities_input_frame, text="Note: Zip codes are not allowed - use city names only", 
                    font=ctk.CTkFont(size=10, slant="italic"), 
                    text_color="gray").pack(pady=(0, 15))
        
        # File selection section
        file_section = ctk.CTkFrame(group_frame)
        file_section.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkLabel(file_section, text="CSV Files Management", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))
        
        file_buttons_frame = ctk.CTkFrame(file_section)
        file_buttons_frame.pack(pady=(0, 15))
        
        self.widgets['browse_csv_btn'] = ctk.CTkButton(
            file_buttons_frame, 
            text="📂 Browse CSV Files", 
            width=140, height=36, 
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.widgets['browse_csv_btn'].pack(side="left", padx=(20, 10), pady=10)
        
        self.widgets['use_default_csv_btn'] = ctk.CTkButton(
            file_buttons_frame, 
            text="📋 Use Group CSVs", 
            width=140, height=36, 
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.widgets['use_default_csv_btn'].pack(side="left", padx=(0, 10), pady=10)
        
        self.widgets['auto_detect_csv_btn'] = ctk.CTkButton(
            file_buttons_frame, 
            text="🔍 Auto-Detect CSVs", 
            width=140, height=36, 
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.widgets['auto_detect_csv_btn'].pack(side="left", padx=(0, 20), pady=10)
        
        # Results/Display Section
        results_section = ctk.CTkFrame(group_frame)
        results_section.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        ctk.CTkLabel(results_section, text="Results & Status", 
                    font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 10))
        
        # Display area for results
        self.widgets['group_textbox'] = ctk.CTkTextbox(results_section, font=ctk.CTkFont(size=11))
        self.widgets['group_textbox'].pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Initial message
        initial_message = ("🌤️ Advanced Weather Comparison Tools\n\n"
                          "� CSV Comparison Only: Compare historical data from multiple CSV files\n"
                          "🌐 CSV + Live Weather: Combine historical data with current weather conditions\n"
                          "🎬 Run Demo: See a demonstration with sample data\n\n"
                          "Instructions:\n"
                          "1. Enter cities for live weather data (optional)\n"
                          "2. Choose CSV files or use default group CSVs\n"
                          "3. Click a comparison button to generate graphs\n\n"
                          "Supported CSV format: Date, Time, City, Temperature_F\n"
                          "Generated plots will be saved in the WeatherCap directory.")
        self.widgets['group_textbox'].insert("0.0", initial_message)


    def get_widget(self, widget_name):
        """Get a specific widget by name"""
        return self.widgets.get(widget_name)
    
    def get_all_widgets(self):
        """Get all widget references"""
        return self.widgets
