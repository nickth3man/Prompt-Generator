"""
Header widget for the Prompt Generator application.
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import pyqtSignal
import os


class HeaderWidget(QWidget):
    """Header widget for the application."""
    
    # Signal emitted when theme toggle button is clicked
    theme_toggled = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components."""
        header_layout = QHBoxLayout(self)
        
        title_label = QLabel("Advanced Prompt Generator")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        
        # Theme toggle button
        self.theme_button = QPushButton()
        self.theme_button.setToolTip("Toggle Dark/Light Theme")
        self.theme_button.setFixedSize(32, 32)
        self.theme_button.clicked.connect(self.theme_toggled.emit)
        
        # Set initial icon based on current theme
        self.update_theme_icon("light")  # Default to light theme icon
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.theme_button)
    
    def update_theme_icon(self, theme):
        """Update the theme button icon based on current theme.
        
        Args:
            theme: Current theme ('light' or 'dark')
        """
        # Set icon based on current theme (shows the opposite theme as the action)
        icon_name = "dark_mode.png" if theme == "light" else "light_mode.png"
        
        # Look for icon in resources directory
        resources_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "resources"
        )
        
        icon_path = os.path.join(resources_dir, icon_name)
        
        # Use icon if it exists, otherwise use text
        if os.path.exists(icon_path):
            self.theme_button.setIcon(QIcon(icon_path))
            self.theme_button.setText("")
        else:
            self.theme_button.setText("🌓")  # Moon/sun emoji as fallback
