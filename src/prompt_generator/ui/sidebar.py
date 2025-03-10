"""
Sidebar widget for the Prompt Generator application.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, 
    QPushButton, QLabel
)
from PyQt5.QtCore import pyqtSignal


class SidebarWidget(QWidget):
    """Sidebar widget for category selection."""
    
    category_selected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.category_buttons = []
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components."""
        sidebar_layout = QVBoxLayout(self)
        
        # Category selection
        category_group = QGroupBox("Prompt Categories")
        category_layout = QVBoxLayout()
        
        # Add category buttons
        categories = [
            ("Chain-of-Thought (CoT)", "cot"),
            ("Tree-of-Thoughts (ToT)", "tot"),
            ("Active Prompting", "active"),
            ("Persona-based Prompting", "persona")
        ]
        
        self.category_buttons = []
        for name, code in categories:
            button = QPushButton(name)
            button.setProperty("category", code)
            button.clicked.connect(lambda checked, c=code: self.category_selected.emit(c))
            category_layout.addWidget(button)
            self.category_buttons.append(button)
        
        category_group.setLayout(category_layout)
        
        # Help section
        help_group = QGroupBox("Help & Information")
        help_layout = QVBoxLayout()
        help_text = QLabel("Select a prompt category to begin creating your specialized prompt.")
        help_text.setWordWrap(True)
        help_layout.addWidget(help_text)
        help_group.setLayout(help_layout)
        
        # Add to sidebar
        sidebar_layout.addWidget(category_group)
        sidebar_layout.addWidget(help_group)
        sidebar_layout.addStretch()
