"""
Application Controller Module - Main application coordinator and lifecycle manager
Coordinates between GUI, event handlers, services, and preferences
"""

import customtkinter as ctk
from tkinter import messagebox
from config import WEATHER_API_KEY, DEFAULT_CITY, WINDOW_WIDTH, WINDOW_HEIGHT, DEFAULT_THEME
from core.weather_api import WeatherAPI, WeatherAPIError
from features.city_comparison import CityComparison
from features.forecast_predict import ForecastPredict
from features.weather_history_csv import WeatherHistoryCSV
from ui.gui_components import WeatherGUIComponents
from ui.event_handlers import WeatherEventHandlers
from utils.preferences_manager import PreferencesManager, ThemeManager


class WeatherAppController:
    """Main application controller coordinating all components"""
    
    def __init__(self):
        """Initialize the weather application controller"""
        self.root = None
        self.gui_components = None
        self.event_handlers = None
        self.preferences_manager = None
        self.theme_manager = None
        self.widgets = {}
        
        # Service instances
        self.api = None
        self.city_comparison = None
        self.forecast_predict = None
        self.weather_history = None
        
        # Initialize application
        self._initialize_application()
    
    def _initialize_application(self):
        """Initialize all application components"""
        try:
            # Initialize services
            self._initialize_services()
            
            # Initialize preferences manager first
            self.preferences_manager = PreferencesManager()
            
            # Initialize theme manager with current theme preference
            current_theme = self.preferences_manager.get_preference('theme', DEFAULT_THEME)
            self.theme_manager = ThemeManager(current_theme)
            
            # Setup GUI
            self._setup_gui()
            
            # Setup event handling
            self._setup_event_handling()
            
            # Apply theme and load initial data
            self._finalize_setup()
            
        except WeatherAPIError as e:
            # Show error message and exit gracefully
            messagebox.showerror("API Configuration Error", str(e))
            return
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize application: {str(e)}")
            return
    
    def _initialize_services(self):
        """Initialize all weather-related services"""
        # Initialize weather API
        self.api = WeatherAPI(WEATHER_API_KEY)
        
        # Initialize feature services
        self.city_comparison = CityComparison(self.api)
        self.forecast_predict = ForecastPredict(self.api)
        self.weather_history = WeatherHistoryCSV()
    
    def _setup_gui(self):
        """Setup the graphical user interface"""
        # Don't set appearance mode here - will be set based on user preferences
        ctk.set_default_color_theme("data/red.json")  # defaults are "blue", "green", "dark-blue"
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("WeatherCap - Weather Dashboard")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(1000, 800)
        
        # Initialize GUI components
        preferences = self.preferences_manager.get_all_preferences()
        self.gui_components = WeatherGUIComponents(self.root, preferences)
        
        # Create all GUI widgets
        self.widgets = self.gui_components.setup_main_layout()
    
    def _setup_event_handling(self):
        """Setup event handlers and bind events"""
        # Initialize event handlers
        self.event_handlers = WeatherEventHandlers(
            self.api, 
            self.city_comparison, 
            self.forecast_predict, 
            self.weather_history
        )
        
        # Set widget references
        self.event_handlers.set_widgets(self.widgets)
        
        # Setup custom event handlers first (before binding)
        self._setup_custom_event_handlers()
        
        # Bind events after custom handlers are set up
        self.event_handlers.bind_events()
    
    def _setup_custom_event_handlers(self):
        """Setup custom event handlers that require controller access"""
        # Theme toggle handler
        def handle_theme_toggle():
            # Get new theme state from switch
            is_dark = self.widgets['theme_switch'].get()
            new_theme = 'dark' if is_dark else 'light'
            
            # Apply theme
            self.theme_manager.apply_theme(new_theme)
            self.preferences_manager.update_preference('theme', new_theme)
            
            # Update status
            self.widgets['status_label'].configure(text=f"Switched to {new_theme} mode")
        
        # Save preferences handler
        def handle_save_preferences():
            current_theme = 'dark' if self.widgets['theme_switch'].get() else 'light'
            current_city = self.widgets['city_entry'].get()
            
            success = self.preferences_manager.save_preferences(current_theme, current_city)
            
            if success:
                messagebox.showinfo("Settings", "Preferences saved successfully!")
                self.widgets['status_label'].configure(text="Preferences saved")
            else:
                messagebox.showerror("Error", "Failed to save preferences")
                self.widgets['status_label'].configure(text="Error saving preferences")
        
        # Override the placeholder handlers in event_handlers
        self.event_handlers.handle_theme_toggle = handle_theme_toggle
        self.event_handlers.handle_save_preferences = handle_save_preferences
    
    def _finalize_setup(self):
        """Apply final setup configurations"""
        # Apply theme from preferences (theme manager is already initialized with correct state)
        theme = self.preferences_manager.get_preference('theme', DEFAULT_THEME)
        self.theme_manager.apply_theme(theme)
        
        # Sync the theme switch with the current theme
        if theme == 'dark':
            self.widgets['theme_switch'].select()
        else:
            self.widgets['theme_switch'].deselect()
        
        # Load initial history
        self.event_handlers.handle_load_recent_history()
        
        # Load default city weather after GUI is ready
        default_city = self.preferences_manager.get_preference('default_city', DEFAULT_CITY)
        self.root.after(100, lambda: self.event_handlers.get_weather(default_city))
    
    def run(self):
        """Start the application main loop"""
        # Check if initialization was successful
        if self.root:
            try:
                self.root.mainloop()
            except Exception as e:
                messagebox.showerror("Runtime Error", f"Application error: {str(e)}")
        else:
            # Initialization failed, don't start the app
            print("Application failed to initialize.")
    
    def get_widget(self, widget_name):
        """
        Get a specific widget by name
        """
        return self.widgets.get(widget_name)
    
    def get_preferences_manager(self):
        """Get the preferences manager instance"""
        return self.preferences_manager
    
    def get_theme_manager(self):
        """Get the theme manager instance"""
        return self.theme_manager
