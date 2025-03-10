"""
Stylesheet management for the Prompt Generator application.
Provides theme styling for light and dark modes.
"""

class StylesheetManager:
    """Manages application stylesheets and themes."""
    
    @staticmethod
    def get_stylesheet(theme="light"):
        """Get the appropriate stylesheet based on the theme."""
        if theme == "dark":
            return StylesheetManager.dark_stylesheet()
        else:
            return StylesheetManager.light_stylesheet()
    
    @staticmethod
    def light_stylesheet():
        """Light theme stylesheet."""
        return """
        QMainWindow, QDialog {
            background-color: #f5f5f5;
            color: #333333;
        }
        
        QWidget {
            background-color: #f5f5f5;
            color: #333333;
        }
        
        QLabel {
            color: #333333;
        }
        
        QPushButton {
            background-color: #e0e0e0;
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 5px 10px;
            color: #333333;
        }
        
        QPushButton:hover {
            background-color: #d0d0d0;
        }
        
        QPushButton:pressed {
            background-color: #c0c0c0;
        }
        
        QLineEdit, QTextEdit, QComboBox {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 3px;
            color: #333333;
        }
        
        QGroupBox {
            border: 1px solid #cccccc;
            border-radius: 4px;
            margin-top: 10px;
            font-weight: bold;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }
        
        QSplitter::handle {
            background-color: #cccccc;
        }
        
        QScrollBar:vertical {
            border: none;
            background-color: #f0f0f0;
            width: 10px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #c0c0c0;
            min-height: 20px;
            border-radius: 5px;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        """
    
    @staticmethod
    def dark_stylesheet():
        """Dark theme stylesheet."""
        return """
        QMainWindow, QDialog {
            background-color: #2d2d2d;
            color: #e0e0e0;
        }
        
        QWidget {
            background-color: #2d2d2d;
            color: #e0e0e0;
        }
        
        QLabel {
            color: #e0e0e0;
        }
        
        QPushButton {
            background-color: #3d3d3d;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 5px 10px;
            color: #e0e0e0;
        }
        
        QPushButton:hover {
            background-color: #4d4d4d;
        }
        
        QPushButton:pressed {
            background-color: #5d5d5d;
        }
        
        QLineEdit, QTextEdit, QComboBox {
            background-color: #3d3d3d;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 3px;
            color: #e0e0e0;
        }
        
        QGroupBox {
            border: 1px solid #555555;
            border-radius: 4px;
            margin-top: 10px;
            font-weight: bold;
            color: #e0e0e0;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 3px 0 3px;
        }
        
        QSplitter::handle {
            background-color: #555555;
        }
        
        QScrollBar:vertical {
            border: none;
            background-color: #3d3d3d;
            width: 10px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #5d5d5d;
            min-height: 20px;
            border-radius: 5px;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        """
