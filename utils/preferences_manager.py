"""
Preferences Manager Module - Handles user preferences loading, saving, and management
Separates preference logic from GUI and application controller
"""

import json
import os
from tkinter import messagebox
from config import DEFAULT_THEME, DEFAULT_CITY


class PreferencesManager:
    """Manages user preferences persistence and theme management"""
    
    def __init__(self):
        """Initialize preferences manager"""
        self.prefs_file = "data/user_preferences.json"
        self.preferences = self.load_preferences()
        
    def load_preferences(self):
        """
        Load user preferences from file
        
        Returns:
            dict: User preferences with default values if file doesn't exist
        """
        default_prefs = {
            'theme': DEFAULT_THEME,
            'default_city': DEFAULT_CITY
        }
        
        try:
            if os.path.exists(self.prefs_file):
                with open(self.prefs_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                return default_prefs
        except Exception as e:
            print(f"Error loading preferences: {e}")
            return default_prefs
    
    def save_preferences(self, theme, default_city):
        """
        Save user preferences to file
        
        Args:
            theme (str): Current theme ('light' or 'dark')
            default_city (str): User's preferred default city
            
        Returns:
            bool: True if saved successfully, False otherwise
        """
        prefs = {
            'theme': theme,
            'default_city': default_city
        }
        
        try:
            os.makedirs(os.path.dirname(self.prefs_file), exist_ok=True)
            with open(self.prefs_file, "w", encoding="utf-8") as f:
                json.dump(prefs, f, indent=2)
            
            # Update internal preferences
            self.preferences = prefs
            return True
            
        except Exception as e:
            print(f"Error saving preferences: {e}")
            return False
    
    def get_preference(self, key, default=None):
        """
        Get a specific preference value
        
        Args:
            key (str): The preference key
            default: Default value if key doesn't exist
            
        Returns:
            The preference value or default
        """
        return self.preferences.get(key, default)
    
    def update_preference(self, key, value):
        """
        Update a specific preference in memory (doesn't save to file)
        
        Args:
            key (str): The preference key
            value: The new value
        """
        self.preferences[key] = value
    
    def get_all_preferences(self):
        """
        Get all current preferences
        
        Returns:
            dict: All current preferences
        """
        return self.preferences.copy()


class ThemeManager:
    """Manages application theme changes and persistence"""
    
    def __init__(self, initial_theme='light'):
        """
        Initialize theme manager
        
        Args:
            initial_theme (str): Initial theme ('light' or 'dark')
        """
        self.current_theme = initial_theme
    
    def apply_theme(self, theme):
        """
        Apply the specified theme to the application
        
        Args:
            theme (str): Theme name ('light' or 'dark')
        """
        import customtkinter as ctk
        
        if theme == "dark":
            ctk.set_appearance_mode("dark")
            self.current_theme = 'dark'
        else:
            ctk.set_appearance_mode("light")
            self.current_theme = 'light'
    
    def toggle_theme(self):
        """
        Toggle between light and dark themes
        
        Returns:
            str: The new theme name
        """
        new_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.apply_theme(new_theme)
        return new_theme
    
    def get_current_theme(self):
        """
        Get the current theme name
        
        Returns:
            str: Current theme name
        """
        return self.current_theme
