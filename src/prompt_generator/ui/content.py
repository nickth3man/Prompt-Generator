"""
Content widget for the Prompt Generator application.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QStackedWidget,
    QFileDialog, QMessageBox
)
import json
import os

from .welcome import WelcomeWidget
from .preview import PreviewWidget
from .prompt_forms import (
    ChainOfThoughtForm, TreeOfThoughtsForm,
    ActivePromptForm, PersonaPromptForm
)
from ..models import (
    ChainOfThoughtPrompt, TreeOfThoughtsPrompt,
    ActivePrompt, PersonaPrompt
)


class ContentWidget(QWidget):
    """Main content area widget."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_form = None
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the UI components."""
        self.content_layout = QVBoxLayout(self)
        
        # Stacked widget for different prompt builders
        self.prompt_stack = QStackedWidget()
        
        # Welcome screen
        self.welcome_widget = WelcomeWidget()
        self.prompt_stack.addWidget(self.welcome_widget)
        
        # Create prompt builder widgets
        self.cot_form = ChainOfThoughtForm()
        self.tot_form = TreeOfThoughtsForm()
        self.active_form = ActivePromptForm()
        self.persona_form = PersonaPromptForm()
        
        # Connect signals
        self.cot_form.prompt_updated.connect(self.update_preview)
        self.tot_form.prompt_updated.connect(self.update_preview)
        self.active_form.prompt_updated.connect(self.update_preview)
        self.persona_form.prompt_updated.connect(self.update_preview)
        
        # Add to stack
        self.prompt_stack.addWidget(self.cot_form)
        self.prompt_stack.addWidget(self.tot_form)
        self.prompt_stack.addWidget(self.active_form)
        self.prompt_stack.addWidget(self.persona_form)
        
        # Add to content area
        self.content_layout.addWidget(self.prompt_stack)
        
        # Preview area
        self.preview_widget = PreviewWidget()
        self.content_layout.addWidget(self.preview_widget)
    
    def show_category(self, category_code):
        """Show the form for the selected category."""
        if category_code == "cot":
            self.prompt_stack.setCurrentWidget(self.cot_form)
            self.current_form = self.cot_form
        elif category_code == "tot":
            self.prompt_stack.setCurrentWidget(self.tot_form)
            self.current_form = self.tot_form
        elif category_code == "active":
            self.prompt_stack.setCurrentWidget(self.active_form)
            self.current_form = self.active_form
        elif category_code == "persona":
            self.prompt_stack.setCurrentWidget(self.persona_form)
            self.current_form = self.persona_form
        else:
            self.prompt_stack.setCurrentWidget(self.welcome_widget)
            self.current_form = None
    
    def set_prompt(self, prompt):
        """Set the prompt for the current form."""
        if self.current_form:
            self.current_form.set_prompt(prompt)
    
    def update_preview(self, prompt):
        """Update the preview with the generated prompt text."""
        self.preview_widget.set_preview_text(prompt.generate_text())
    
    def save_current_prompt(self):
        """Save the current prompt to a file."""
        if not self.current_form:
            return
        
        prompt = self.current_form.get_prompt()
        
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix("json")
        file_path, _ = file_dialog.getSaveFileName(
            self, "Save Prompt", "", "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    json.dump(prompt.to_dict(), f, indent=4)
                QMessageBox.information(self, "Success", "Prompt saved successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save prompt: {str(e)}")
    
    def load_prompt(self):
        """Load a prompt from a file."""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, "Load Prompt", "", "JSON Files (*.json)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                prompt_type = data.get("type", "")
                
                if prompt_type == "cot":
                    prompt = ChainOfThoughtPrompt.from_dict(data)
                    self.show_category("cot")
                elif prompt_type == "tot":
                    prompt = TreeOfThoughtsPrompt.from_dict(data)
                    self.show_category("tot")
                elif prompt_type == "active":
                    prompt = ActivePrompt.from_dict(data)
                    self.show_category("active")
                elif prompt_type == "persona":
                    prompt = PersonaPrompt.from_dict(data)
                    self.show_category("persona")
                else:
                    QMessageBox.warning(self, "Warning", "Unknown prompt type.")
                    return
                
                self.set_prompt(prompt)
                self.update_preview(prompt)
                
                QMessageBox.information(self, "Success", "Prompt loaded successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load prompt: {str(e)}")
    
    def export_current_prompt(self):
        """Export the current prompt to a text file."""
        if not self.current_form:
            return
        
        prompt = self.current_form.get_prompt()
        
        file_dialog = QFileDialog()
        file_dialog.setDefaultSuffix("txt")
        file_path, _ = file_dialog.getSaveFileName(
            self, "Export Prompt", "", "Text Files (*.txt)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(prompt.generate_text())
                QMessageBox.information(self, "Success", "Prompt exported successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export prompt: {str(e)}")
    
    def clear_current_form(self):
        """Clear the current form."""
        if self.current_form:
            category_code = self.current_form.get_prompt().type
            
            if category_code == "cot":
                self.current_form.set_prompt(ChainOfThoughtPrompt())
            elif category_code == "tot":
                self.current_form.set_prompt(TreeOfThoughtsPrompt())
            elif category_code == "active":
                self.current_form.set_prompt(ActivePrompt())
            elif category_code == "persona":
                self.current_form.set_prompt(PersonaPrompt())
