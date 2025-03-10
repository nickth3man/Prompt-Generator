"""
Theme management for the Prompt Generator application.
Provides functionality for switching between light and dark themes.
"""

from PyQt5.QtWidgets import QApplication
from .stylesheets import StylesheetManager
from .settings import Settings


class ThemeManager:
    """Manages application themes and provides theme switching functionality."""
    
    def __init__(self):
        """Initialize the theme manager."""
        self.settings = Settings()
        self.current_theme = self.settings.get("theme")
    
    def get_current_theme(self):
        """Get the current theme."""
        return self.current_theme
    
    def toggle_theme(self):
        """Toggle between light and dark themes."""
        if self.current_theme == "light":
            self.set_theme("dark")
        else:
            self.set_theme("light")
        return self.current_theme
    
    def set_theme(self, theme):
        """Set the application theme."""
        if theme not in ["light", "dark"]:
            return False
        
        self.current_theme = theme
        self.settings.set("theme", theme)
        
        # Apply stylesheet to the application
        app = QApplication.instance()
        if app:
            app.setStyleSheet(StylesheetManager.get_stylesheet(theme))
        
        return True
    
    def apply_current_theme(self):
        """Apply the current theme to the application."""
        app = QApplication.instance()
        if app:
            app.setStyleSheet(StylesheetManager.get_stylesheet(self.current_theme))
