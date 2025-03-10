"""
Keyboard shortcuts management for the Prompt Generator application.
Provides functionality for registering and handling keyboard shortcuts.
"""

from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QKeySequence
from .settings import Settings


class ShortcutManager:
    """Manages application keyboard shortcuts."""
    
    def __init__(self, parent=None):
        """Initialize the shortcut manager.
        
        Args:
            parent: The parent widget to attach shortcuts to
        """
        self.parent = parent
        self.settings = Settings()
        self.shortcuts = {}
        self.actions = {}
    
    def register_action(self, action_name, callback):
        """Register an action with a callback function.
        
        Args:
            action_name: Name of the action
            callback: Function to call when shortcut is triggered
        """
        self.actions[action_name] = callback
    
    def register_shortcuts(self):
        """Register all shortcuts from settings."""
        if not self.parent:
            return
        
        # Get shortcuts from settings
        shortcuts_dict = self.settings.get("keyboard_shortcuts")
        
        # Create shortcuts
        for action_name, key_sequence in shortcuts_dict.items():
            if action_name in self.actions:
                shortcut = QShortcut(QKeySequence(key_sequence), self.parent)
                shortcut.activated.connect(self.actions[action_name])
                self.shortcuts[action_name] = shortcut
    
    def update_shortcut(self, action_name, key_sequence):
        """Update a shortcut key sequence.
        
        Args:
            action_name: Name of the action
            key_sequence: New key sequence for the shortcut
        """
        # Update in settings
        shortcuts_dict = self.settings.get("keyboard_shortcuts")
        shortcuts_dict[action_name] = key_sequence
        self.settings.set("keyboard_shortcuts", shortcuts_dict)
        
        # Update active shortcut if it exists
        if action_name in self.shortcuts:
            self.shortcuts[action_name].setKey(QKeySequence(key_sequence))
    
    def get_shortcut_text(self, action_name):
        """Get the text representation of a shortcut.
        
        Args:
            action_name: Name of the action
            
        Returns:
            String representation of the shortcut key sequence
        """
        shortcuts_dict = self.settings.get("keyboard_shortcuts")
        return shortcuts_dict.get(action_name, "")
