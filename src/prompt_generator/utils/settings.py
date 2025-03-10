"""
Settings management for the Prompt Generator application.
Handles user preferences, theme settings, and application configuration.
"""

import json
import os
from PyQt5.QtCore import QSettings


class Settings:
    """Manages application settings and preferences."""

    
    def __init__(self):
        self.settings = QSettings("PromptGenerator", "PromptGeneratorApp")
        self.default_settings = {
            "theme": "light",  # light or dark
            "font_size": 10,
            "save_history": True,
            "max_history_items": 50,
            "default_export_format": "txt",
            "export_formats": ["txt", "md", "html", "json"],
            "window_size": (1000, 700),
            "sidebar_width": 200,
            "keyboard_shortcuts": {
                "save": "Ctrl+S",
                "load": "Ctrl+O",
                "export": "Ctrl+E",
                "clear": "Ctrl+N",
                "toggle_theme": "Ctrl+T",
                "preview": "Ctrl+P",
                "copy_to_clipboard": "Ctrl+C"
            },
            "auto_save": True,
            "auto_save_interval": 5  # minutes
        }

        # Initialize settings if they don't exist
        if not self.settings.contains("theme"):
            self.reset_to_defaults()

            "window_size": (1000, 700),
            "sidebar_width": 200
        }
        
        # Initialize settings if they don't exist
        if not self.settings.contains("theme"):
            self.reset_to_defaults()
    
    def get(self, key):
        """Get a setting value."""
        if key in self.default_settings:
            value_type = type(self.default_settings[key])

            if value_type == bool:
                return self.settings.value(
                    key, self.default_settings[key], type=bool
                )
            elif value_type == int:
                return self.settings.value(
                    key, self.default_settings[key], type=int
                )
            elif value_type == float:
                return self.settings.value(
                    key, self.default_settings[key], type=float
                )
            
            if value_type == bool:
                return self.settings.value(key, self.default_settings[key], type=bool)
            elif value_type == int:
                return self.settings.value(key, self.default_settings[key], type=int)
            elif value_type == float:
                return self.settings.value(key, self.default_settings[key], type=float)
            elif value_type == tuple:
                # Handle tuple conversion
                value = self.settings.value(key, self.default_settings[key])
                if isinstance(value, str):
                    # Convert from string if needed
                    try:
                        return tuple(map(int, value.strip('()').split(',')))
                    except ValueError:
                        return self.default_settings[key]
                return value
            elif value_type == dict:
                # Handle dictionary conversion
                value = self.settings.value(key, self.default_settings[key])
                if isinstance(value, str):
                    # Convert from string if needed
                    try:
                        return dict(
                            item.split(": ")
                            for item in value.strip("{}").split(", ")
                        )
                    except ValueError:
                    except:
                        return self.default_settings[key]
                return value
            else:
                return self.settings.value(key, self.default_settings[key])
        return None

    
    def set(self, key, value):
        """Set a setting value."""
        if key in self.default_settings:
            self.settings.setValue(key, value)
            self.settings.sync()
            return True
        return False

    
    def reset_to_defaults(self):
        """Reset all settings to default values."""
        for key, value in self.default_settings.items():
            self.settings.setValue(key, value)
        self.settings.sync()

    
    def export_settings(self, filepath):
        """Export settings to a JSON file."""
        settings_dict = {}
        for key in self.default_settings.keys():
            settings_dict[key] = self.get(key)

        with open(filepath, 'w') as f:
            json.dump(settings_dict, f, indent=4)

        
        with open(filepath, 'w') as f:
            json.dump(settings_dict, f, indent=4)
    
    def import_settings(self, filepath):
        """Import settings from a JSON file."""
        if not os.path.exists(filepath):
            return False

        try:
            with open(filepath, 'r') as f:
                settings_dict = json.load(f)

        
        try:
            with open(filepath, 'r') as f:
                settings_dict = json.load(f)
            
            for key, value in settings_dict.items():
                if key in self.default_settings:
                    self.set(key, value)
            return True
        except Exception as e:
            print(f"Error importing settings: {e}")
        except:
            return False
