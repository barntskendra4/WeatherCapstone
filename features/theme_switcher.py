import tkinter as tk
import customtkinter as ctk
import json
import os

class ThemeSwitcher:
    """Handles theme switching for the CustomTkinter application"""
    
    def __init__(self):
        # CustomTkinter uses appearance modes and color themes
        self.current_theme = "light"
        
        # Load custom themes from JSON file
        self.custom_colors = self.load_themes_from_json()
    
    def load_themes_from_json(self):
        """Load custom themes from JSON file"""
        themes_file = "data/custom_themes.json"
        
        # Fallback themes in case JSON file doesn't exist
        fallback_themes = {
            "purple": {
                "CTkFrame": {"fg_color": ["#F5F5F5", "#1A1A1A"]},
                "CTkButton": {
                    "fg_color": ["#7404ec", "#9966ff"],
                    "hover_color": ["#5c03b8", "#7a4dff"],
                    "text_color": ["white", "white"]
                },
                "CTkEntry": {
                    "fg_color": ["#FFFFFF", "#2D2D2D"],
                    "border_color": ["#7404ec", "#9966ff"]
                },
                "CTkTextbox": {
                    "fg_color": ["#FFFFFF", "#2D2D2D"]
                }
            }
        }
        
        try:
            if os.path.exists(themes_file):
                with open(themes_file, 'r', encoding='utf-8') as f:
                    themes_data = json.load(f)
                    return themes_data.get('themes', fallback_themes)
            else:
                print(f"Themes file not found: {themes_file}, using fallback themes")
                return fallback_themes
        except Exception as e:
            print(f"Error loading themes: {e}, using fallback themes")
            return fallback_themes
    
    def apply_theme(self, theme_name):
        """Apply the specified theme to the CustomTkinter application"""
        print(f"Applying theme: {theme_name}")
        
        if theme_name in ["light", "dark"]:
            # Use built-in appearance modes
            ctk.set_appearance_mode(theme_name)
            # Reset to default blue theme for built-in modes
            ctk.set_default_color_theme("blue")
            self.current_theme = theme_name
            print(f"Applied built-in theme: {theme_name}")
        elif theme_name in self.custom_colors:
            # Apply custom color theme
            self._apply_custom_colors(theme_name)
            self.current_theme = theme_name
        else:
            # Default to light mode
            ctk.set_appearance_mode("light")
            ctk.set_default_color_theme("data/purple_theme.json")
            self.current_theme = "light"
            print("Applied default light theme")
    
    def _apply_custom_colors(self, color_theme):
        """Apply custom color scheme by creating and loading a custom theme file"""
        if color_theme in self.custom_colors:
            colors = self.custom_colors[color_theme]
            
            try:
                # Create a temporary theme file for CustomTkinter
                theme_file_path = f"data/temp_{color_theme}_theme.json"
                self._create_ctk_theme_file(colors, theme_file_path)
                
                # Load the custom theme
                ctk.set_default_color_theme(theme_file_path)
                
                # Set appearance mode to light to see the first color values
                ctk.set_appearance_mode("light")
                
                print(f"Applied custom theme: {color_theme}")
                
            except Exception as e:
                print(f"Error applying custom theme {color_theme}: {e}")
                # Fallback: Set a predefined color theme that's closest to our custom theme
                if color_theme in ["purple", "lavender"]:
                    ctk.set_default_color_theme("blue")  # Blue is closest to purple
                elif color_theme in ["emerald", "mint"]:
                    ctk.set_default_color_theme("green")
                elif color_theme in ["crimson", "rose_gold", "sunset"]:
                    ctk.set_default_color_theme("blue")  # No red default, use blue
                elif color_theme == "ocean":
                    ctk.set_default_color_theme("dark-blue")
                else:
                    ctk.set_default_color_theme("blue")
    
    def _create_ctk_theme_file(self, colors, file_path):
        """Create a CustomTkinter-compatible theme file"""
        # Get the base theme structure from a template
        base_theme = {
            "CTk": {
                "fg_color": ["gray95", "gray10"]
            },
            "CTkToplevel": {
                "fg_color": ["gray95", "gray10"]
            },
            "CTkFrame": {
                "corner_radius": 6,
                "border_width": 0,
                "fg_color": ["gray95", "gray10"],
                "top_fg_color": ["gray85", "gray15"],
                "border_color": ["#979DA2", "#565B5E"]
            },
            "CTkButton": {
                "corner_radius": 6,
                "border_width": 0,
                "fg_color": ["#72D03B", "#1F538D"],
                "hover_color": ["#FD00EC", "#144870"],
                "border_color": ["#3E454A", "#949A9F"],
                "text_color": ["white", "white"],
                "text_color_disabled": ["gray74", "gray60"]
            },
            "CTkLabel": {
                "corner_radius": 0,
                "fg_color": "transparent",
                "text_color": ["gray10", "#DCE4EE"]
            },
            "CTkEntry": {
                "corner_radius": 6,
                "border_width": 2,
                "fg_color": ["#F9F9FA", "#343638"],
                "border_color": ["#979DA2", "#565B5E"],
                "text_color": ["gray10", "#DCE4EE"],
                "placeholder_text_color": ["gray52", "gray62"]
            },
            "CTkTextbox": {
                "corner_radius": 6,
                "border_width": 0,
                "fg_color": ["#F9F9FA", "#343638"],
                "border_color": ["#979DA2", "#565B5E"],
                "text_color": ["gray10", "#DCE4EE"],
                "scrollbar_button_color": ["gray55", "gray41"],
                "scrollbar_button_hover_color": ["gray40", "gray53"]
            },
            "CTkComboBox": {
                "corner_radius": 6,
                "border_width": 2,
                "fg_color": ["#F9F9FA", "#343638"],
                "border_color": ["#979DA2", "#565B5E"],
                "button_color": ["#979DA2", "#565B5E"],
                "button_hover_color": ["gray70", "gray41"],
                "text_color": ["gray10", "#DCE4EE"],
                "text_color_disabled": ["gray50", "gray45"]
            }
        }
        
        # Update the base theme with our custom colors
        if "CTkFrame" in colors:
            if "fg_color" in colors["CTkFrame"]:
                base_theme["CTkFrame"]["fg_color"] = colors["CTkFrame"]["fg_color"]
                base_theme["CTk"]["fg_color"] = colors["CTkFrame"]["fg_color"]
                base_theme["CTkToplevel"]["fg_color"] = colors["CTkFrame"]["fg_color"]
        
        if "CTkButton" in colors:
            base_theme["CTkButton"].update(colors["CTkButton"])
            
        if "CTkEntry" in colors:
            base_theme["CTkEntry"].update(colors["CTkEntry"])
            
        if "CTkTextbox" in colors:
            base_theme["CTkTextbox"].update(colors["CTkTextbox"])
            
        if "CTkComboBox" in colors:
            base_theme["CTkComboBox"].update(colors["CTkComboBox"])
        
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write the theme file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(base_theme, f, indent=2)
    
    def get_available_themes(self):
        """Get list of available theme names"""
        return ["light", "dark"] + list(self.custom_colors.keys())
    
    def get_theme_info(self, theme_name):
        """Get detailed information about a theme"""
        if theme_name in ["light", "dark"]:
            return f"Built-in {theme_name} appearance mode"
        elif theme_name in self.custom_colors:
            return f"Custom {theme_name.replace('_', ' ').title()} theme"
        else:
            return "Unknown theme"
    
    def reload_themes(self):
        """Reload themes from JSON file"""
        self.custom_colors = self.load_themes_from_json()
        return self.get_available_themes()
    
    def get_current_theme(self):
        """Get the current theme name"""
        return self.current_theme
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        if self.current_theme == "light":
            self.apply_theme("dark")
        else:
            self.apply_theme("light")
        return self.current_theme
    
    def refresh_widgets(self, root_widget):
        """Refresh all widgets to apply new theme (experimental)"""
        try:
            # This is a workaround since CustomTkinter themes only apply to new widgets
            # For now, we'll just print a message
            print("Note: Theme changes may require application restart to fully apply to all widgets")
            print("New widgets created after theme change will use the new colors")
        except Exception as e:
            print(f"Widget refresh error: {e}")
    
    def get_theme_preview_colors(self, theme_name):
        """Get preview colors for a theme"""
        if theme_name in ["light", "dark"]:
            if theme_name == "light":
                return {"bg": "#FFFFFF", "accent": "#1f538d"}
            else:
                return {"bg": "#212121", "accent": "#1f538d"}
        elif theme_name in self.custom_colors:
            colors = self.custom_colors[theme_name]
            button_colors = colors.get("CTkButton", {}).get("fg_color", ["#1f538d", "#1f538d"])
            frame_colors = colors.get("CTkFrame", {}).get("fg_color", ["#FFFFFF", "#212121"])
            return {
                "bg": frame_colors[0], 
                "accent": button_colors[0]
            }
        return {"bg": "#FFFFFF", "accent": "#1f538d"}
    
    def apply_theme_with_restart_warning(self, theme_name, show_warning=True):
        """Apply theme and show restart warning if needed"""
        old_theme = self.current_theme
        self.apply_theme(theme_name)
        
        if old_theme != theme_name and theme_name not in ["light", "dark"] and show_warning:
            return "restart_needed"
        return "applied"

