"""
Preview widget for the Prompt Generator application.
"""

from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QTextEdit


class PreviewWidget(QGroupBox):
    """Preview widget for displaying generated prompts."""
    
    def __init__(self, parent=None):
        super().__init__("Prompt Preview", parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components."""
        preview_layout = QVBoxLayout(self)
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMinimumHeight(200)
        
        preview_layout.addWidget(self.preview_text)
    
    def set_preview_text(self, text):
        """Set the preview text."""
        self.preview_text.setPlainText(text)
