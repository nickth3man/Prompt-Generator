"""
Welcome screen widget for the Prompt Generator application.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont


class WelcomeWidget(QWidget):
    """Welcome screen widget."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components."""
        welcome_layout = QVBoxLayout(self)
        
        welcome_title = QLabel("Welcome to the Advanced Prompt Generator")
        welcome_title.setFont(QFont("Arial", 14, QFont.Bold))
        
        welcome_description = QLabel(
            "This tool will help you create effective prompts for AI-assisted content creation.\n\n"
            "Choose a prompt category from the left sidebar to get started:\n"
            "• Chain-of-Thought (CoT): Break complex topics into logical sequential steps\n"
            "• Tree-of-Thoughts (ToT): Explore multiple solution paths simultaneously\n"
            "• Active Prompting: Utilize iterative refinement based on feedback\n"
            "• Persona-based Prompting: Leverage role assumption for specialized expertise\n\n"
            "Each generator will guide you through creating a prompt optimized for your L&D needs."
        )
        welcome_description.setWordWrap(True)
        
        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_description)
        welcome_layout.addStretch()
