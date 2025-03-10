"""
History management for the Prompt Generator application.
Provides functionality for tracking and managing prompt history.
"""

import json
import os
from datetime import datetime
from .settings import Settings


class HistoryManager:
    """Manages prompt history tracking."""
    
    def __init__(self):
        """Initialize the history manager."""
        self.settings = Settings()
        self.history_enabled = self.settings.get("save_history")
        self.max_items = self.settings.get("max_history_items")
        self.history_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "prompt_history.json"
        )
        self.history = self._load_history()
    
    def _load_history(self):
        """Load history from file."""
        if not self.history_enabled:
            return []
        
        if not os.path.exists(self.history_file):
            return []
        
        try:
            with open(self.history_file, 'r') as f:
                history = json.load(f)
            return history
        except Exception as e:
            print(f"Error loading history: {e}")
            return []
    
    def _save_history(self):
        """Save history to file."""
        if not self.history_enabled:
            return
        
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            print(f"Error saving history: {e}")
    
    def add_to_history(self, prompt_data):
        """Add a prompt to history.
        
        Args:
            prompt_data: Dictionary containing prompt data
        """
        if not self.history_enabled:
            return
        
        # Add timestamp if not present
        if "timestamp" not in prompt_data:
            prompt_data["timestamp"] = datetime.now().isoformat()
        
        # Add to history
        self.history.insert(0, prompt_data)
        
        # Limit history size
        if len(self.history) > self.max_items:
            self.history = self.history[:self.max_items]
        
        # Save history
        self._save_history()
    
    def get_history(self):
        """Get the prompt history.
        
        Returns:
            List of prompt history items
        """
        return self.history
    
    def clear_history(self):
        """Clear the prompt history."""
        self.history = []
        self._save_history()
    
    def remove_from_history(self, index):
        """Remove a prompt from history.
        
        Args:
            index: Index of the prompt to remove
        """
        if 0 <= index < len(self.history):
            del self.history[index]
            self._save_history()
    
    def enable_history(self, enabled=True):
        """Enable or disable history tracking.
        
        Args:
            enabled: Whether history tracking should be enabled
        """
        self.history_enabled = enabled
        self.settings.set("save_history", enabled)
    
    def set_max_items(self, max_items):
        """Set the maximum number of history items.
        
        Args:
            max_items: Maximum number of history items to keep
        """
        self.max_items = max_items
        self.settings.set("max_history_items", max_items)
        
        # Trim history if needed
        if len(self.history) > self.max_items:
            self.history = self.history[:self.max_items]
            self._save_history()
