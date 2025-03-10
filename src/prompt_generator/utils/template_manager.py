"""
Template management for the Prompt Generator application.
Provides functionality for saving, loading, and managing prompt templates.
"""

import json
import os
from datetime import datetime
from .settings import Settings


class TemplateManager:
    """Manages prompt templates."""
    
    def __init__(self):
        """Initialize the template manager."""
        self.settings = Settings()
        self.templates_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            "templates"
        )
        
        # Create templates directory if it doesn't exist
        if not os.path.exists(self.templates_dir):
            os.makedirs(self.templates_dir)
        
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """Load templates from the templates directory."""
        templates = {}
        
        if not os.path.exists(self.templates_dir):
            return templates
        
        # Load templates from each file in the templates directory
        for filename in os.listdir(self.templates_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(self.templates_dir, filename), 'r') as f:
                        template = json.load(f)
                    
                    # Use template ID as key, or filename if ID not present
                    template_id = template.get('id', filename[:-5])
                    templates[template_id] = template
                except Exception as e:
                    print(f"Error loading template {filename}: {e}")
        
        return templates
    
    def save_template(self, template_data):
        """Save a template.
        
        Args:
            template_data: Dictionary containing template data
            
        Returns:
            Template ID if successful, None otherwise
        """
        # Generate a template ID if not present
        if 'id' not in template_data:
            template_data['id'] = f"template_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Add timestamp if not present
        if 'created_at' not in template_data:
            template_data['created_at'] = datetime.now().isoformat()
        template_data['updated_at'] = datetime.now().isoformat()
        
        # Save template to file
        template_id = template_data['id']
        filename = f"{template_id}.json"
        
        try:
            with open(os.path.join(self.templates_dir, filename), 'w') as f:
                json.dump(template_data, f, indent=4)
            
            # Add to templates dictionary
            self.templates[template_id] = template_data
            return template_id
        except Exception as e:
            print(f"Error saving template: {e}")
            return None
    
    def get_template(self, template_id):
        """Get a template by ID.
        
        Args:
            template_id: ID of the template to get
            
        Returns:
            Template data if found, None otherwise
        """
        return self.templates.get(template_id)
    
    def get_all_templates(self):
        """Get all templates.
        
        Returns:
            Dictionary of all templates
        """
        return self.templates
    
    def delete_template(self, template_id):
        """Delete a template.
        
        Args:
            template_id: ID of the template to delete
            
        Returns:
            True if successful, False otherwise
        """
        if template_id not in self.templates:
            return False
        
        # Delete template file
        filename = f"{template_id}.json"
        filepath = os.path.join(self.templates_dir, filename)
        
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
                # Remove from templates dictionary
                del self.templates[template_id]
                return True
            except Exception as e:
                print(f"Error deleting template: {e}")
                return False
        
        return False
    
    def update_template(self, template_id, template_data):
        """Update a template.
        
        Args:
            template_id: ID of the template to update
            template_data: New template data
            
        Returns:
            True if successful, False otherwise
        """
        if template_id not in self.templates:
            return False
        
        # Update template data
        template_data['id'] = template_id
        template_data['updated_at'] = datetime.now().isoformat()
        
        # Preserve creation timestamp
        if 'created_at' not in template_data and 'created_at' in self.templates[template_id]:
            template_data['created_at'] = self.templates[template_id]['created_at']
        
        # Save updated template
        return self.save_template(template_data) is not None
