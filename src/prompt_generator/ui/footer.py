"""
Footer widget for the Prompt Generator application.
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton


class FooterWidget(QWidget):
    """Footer widget with action buttons."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components."""
        footer_layout = QHBoxLayout(self)
        
        # Add buttons
        self.save_button = QPushButton("Save Prompt")
        self.load_button = QPushButton("Load Prompt")
        self.export_button = QPushButton("Export Prompt")
        self.clear_button = QPushButton("Clear Form")
        
        footer_layout.addWidget(self.save_button)
        footer_layout.addWidget(self.load_button)
        footer_layout.addWidget(self.export_button)
        footer_layout.addStretch()
        footer_layout.addWidget(self.clear_button)
    
    @property
    def save_clicked(self):
        """Get the save button clicked signal."""
        return self.save_button.clicked
    
    @property
    def load_clicked(self):
        """Get the load button clicked signal."""
        return self.load_button.clicked
    
    @property
    def export_clicked(self):
        """Get the export button clicked signal."""
        return self.export_button.clicked
    
    @property
    def clear_clicked(self):
        """Get the clear button clicked signal."""
        return self.clear_button.clicked
