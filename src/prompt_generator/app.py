"""
Main application module for the Prompt Generator.
Defines the main window and application logic.
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QSplitter
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from .ui.header import HeaderWidget
from .ui.sidebar import SidebarWidget
from .ui.content import ContentWidget
from .ui.footer import FooterWidget
from .models import (
    ChainOfThoughtPrompt, TreeOfThoughtsPrompt,
    ActivePrompt, PersonaPrompt
)
from .utils.settings import Settings


class PromptGeneratorApp(QMainWindow):
    """Main application window for the Prompt Generator."""
    
    def __init__(self):
        super().__init__()
        self.settings = Settings()
        self.setWindowTitle("Advanced Prompt Generator for L&D Professionals")
        self.setMinimumSize(*self.settings.get("window_size"))
        
        # Set application icon
        icon_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "app_icon.ico"
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Initialize UI components
        self.setup_ui()
        
        # Initialize data
        self.current_prompt_data = {}
        self.initialize_prompt_templates()
    
    def setup_ui(self):
        """Set up the main UI components."""
        # Header
        self.header = HeaderWidget()
        self.main_layout.addWidget(self.header)
        
        # Content splitter
        self.splitter = QSplitter(Qt.Horizontal)
        
        # Sidebar
        self.sidebar = SidebarWidget()
        self.sidebar.category_selected.connect(self.select_category)
        
        # Content area
        self.content = ContentWidget()
        
        # Add to splitter
        self.splitter.addWidget(self.sidebar)
        self.splitter.addWidget(self.content)
        sidebar_width = self.settings.get("sidebar_width")
        window_width = self.settings.get("window_size")[0]
        self.splitter.setSizes([
            sidebar_width,
            window_width - sidebar_width
        ])
        
        # Add splitter to main layout
        self.main_layout.addWidget(self.splitter)
        
        # Footer
        self.footer = FooterWidget()
        self.footer.save_clicked.connect(self.save_prompt)
        self.footer.load_clicked.connect(self.load_prompt)
        self.footer.export_clicked.connect(self.export_prompt)
        self.footer.clear_clicked.connect(self.clear_form)
        self.main_layout.addWidget(self.footer)
    
    def initialize_prompt_templates(self):
        """Initialize prompt templates."""
        # Create default templates
        self.prompt_templates = {
            "cot": ChainOfThoughtPrompt(),
            "tot": TreeOfThoughtsPrompt(),
            "active": ActivePrompt(),
            "persona": PersonaPrompt()
        }
    
    def select_category(self, category_code):
        """Handle category selection."""
        self.content.show_category(category_code)
        
        # Set current prompt data
        if category_code in self.prompt_templates:
            self.current_prompt_data = self.prompt_templates[category_code]
            self.content.set_prompt(self.current_prompt_data)
    
    def update_preview(self, prompt):
        """Update the preview area with generated prompt text."""
        self.content.update_preview(prompt.generate_text())
    
    def save_prompt(self):
        """Save the current prompt."""
        self.content.save_current_prompt()
    
    def load_prompt(self):
        """Load a saved prompt."""
        self.content.load_prompt()
    
    def export_prompt(self):
        """Export the current prompt to a file."""
        self.content.export_current_prompt()
    
    def clear_form(self):
        """Clear the current form."""
        self.content.clear_current_form()


def run_application():
    """Run the Prompt Generator application."""
    app = QApplication(sys.argv)
    window = PromptGeneratorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    run_application()
