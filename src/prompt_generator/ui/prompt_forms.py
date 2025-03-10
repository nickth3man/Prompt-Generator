"""
Prompt form widgets for the Prompt Generator application.
Provides UI components for different prompt types.
"""

from PyQt5.QtWidgets import (
    QWidget, QFormLayout, QLineEdit, QTextEdit, 
    QComboBox, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QGroupBox
)
from PyQt5.QtCore import pyqtSignal

from ..models import (
    BasePrompt, ChainOfThoughtPrompt, TreeOfThoughtsPrompt,
    ActivePrompt, PersonaPrompt
)


class BasePromptForm(QWidget):
    """Base class for all prompt form widgets."""
    
    prompt_updated = pyqtSignal(BasePrompt)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.prompt = None
        self.fields = {}
        
        self.setup_ui()
        self.connect_signals()
    
    def setup_ui(self):
        """Set up the UI components."""
        self.layout = QFormLayout(self)
    
    def connect_signals(self):
        """Connect signals to slots."""
        pass
    
    def set_prompt(self, prompt):
        """Set the prompt and update the form fields."""
        self.prompt = prompt
        self.update_fields_from_prompt()
    
    def get_prompt(self):
        """Get the current prompt with updated values."""
        self.update_prompt_from_fields()
        return self.prompt
    
    def update_fields_from_prompt(self):
        """Update form fields from prompt data."""
        pass
    
    def update_prompt_from_fields(self):
        """Update prompt data from form fields."""
        pass
    
    def clear_fields(self):
        """Clear all form fields."""
        for field in self.fields.values():
            if isinstance(field, QLineEdit):
                field.clear()
            elif isinstance(field, QTextEdit):
                field.clear()
            elif isinstance(field, QComboBox):
                field.setCurrentIndex(0)
    
    def field_changed(self):
        """Handle field changes."""
        if self.prompt:
            self.update_prompt_from_fields()
            self.prompt_updated.emit(self.prompt)


class ChainOfThoughtForm(BasePromptForm):
    """Form for Chain of Thought prompts."""
    
    def setup_ui(self):
        """Set up the UI components."""
        super().setup_ui()
        
        # Topic
        self.fields["topic"] = QLineEdit()
        self.layout.addRow("Topic:", self.fields["topic"])
        
        # Audience
        self.fields["audience"] = QLineEdit()
        self.layout.addRow("Audience:", self.fields["audience"])
        
        # Learning Objective
        self.fields["objective"] = QTextEdit()
        self.fields["objective"].setMaximumHeight(80)
        self.layout.addRow("Learning Objective:", self.fields["objective"])
        
        # Reasoning Steps
        self.fields["steps"] = QTextEdit()
        self.layout.addRow("Reasoning Steps:", self.fields["steps"])
        
        # Format
        self.fields["format"] = QLineEdit()
        self.layout.addRow("Format:", self.fields["format"])
        
        # Length
        self.fields["length"] = QLineEdit()
        self.layout.addRow("Length:", self.fields["length"])
    
    def connect_signals(self):
        """Connect signals to slots."""
        for field in self.fields.values():
            if isinstance(field, QLineEdit):
                field.textChanged.connect(self.field_changed)
            elif isinstance(field, QTextEdit):
                field.textChanged.connect(self.field_changed)
    
    def update_fields_from_prompt(self):
        """Update form fields from prompt data."""
        if not isinstance(self.prompt, ChainOfThoughtPrompt):
            return
        
        self.fields["topic"].setText(self.prompt.topic)
        self.fields["audience"].setText(self.prompt.audience)
        self.fields["objective"].setPlainText(self.prompt.objective)
        self.fields["steps"].setPlainText(self.prompt.steps)
        self.fields["format"].setText(self.prompt.format)
        self.fields["length"].setText(self.prompt.length)
    
    def update_prompt_from_fields(self):
        """Update prompt data from form fields."""
        if not isinstance(self.prompt, ChainOfThoughtPrompt):
            self.prompt = ChainOfThoughtPrompt()
        
        self.prompt.topic = self.fields["topic"].text()
        self.prompt.audience = self.fields["audience"].text()
        self.prompt.objective = self.fields["objective"].toPlainText()
        self.prompt.steps = self.fields["steps"].toPlainText()
        self.prompt.format = self.fields["format"].text()
        self.prompt.length = self.fields["length"].text()


class TreeOfThoughtsForm(BasePromptForm):
    """Form for Tree of Thoughts prompts."""
    
    def setup_ui(self):
        """Set up the UI components."""
        super().setup_ui()
        
        # Topic
        self.fields["topic"] = QLineEdit()
        self.layout.addRow("Topic:", self.fields["topic"])
        
        # Audience
        self.fields["audience"] = QLineEdit()
        self.layout.addRow("Audience:", self.fields["audience"])
        
        # Learning Objective
        self.fields["objective"] = QTextEdit()
        self.fields["objective"].setMaximumHeight(80)
        self.layout.addRow("Learning Objective:", self.fields["objective"])
        
        # Thought Branches
        self.fields["branches"] = QTextEdit()
        self.layout.addRow("Thought Branches:", self.fields["branches"])
        
        # Evaluation Criteria
        self.fields["evaluation"] = QTextEdit()
        self.fields["evaluation"].setMaximumHeight(80)
        self.layout.addRow("Evaluation Criteria:", self.fields["evaluation"])
        
        # Format
        self.fields["format"] = QLineEdit()
        self.layout.addRow("Format:", self.fields["format"])
        
        # Length
        self.fields["length"] = QLineEdit()
        self.layout.addRow("Length:", self.fields["length"])
    
    def connect_signals(self):
        """Connect signals to slots."""
        for field in self.fields.values():
            if isinstance(field, QLineEdit):
                field.textChanged.connect(self.field_changed)
            elif isinstance(field, QTextEdit):
                field.textChanged.connect(self.field_changed)
    
    def update_fields_from_prompt(self):
        """Update form fields from prompt data."""
        if not isinstance(self.prompt, TreeOfThoughtsPrompt):
            return
        
        self.fields["topic"].setText(self.prompt.topic)
        self.fields["audience"].setText(self.prompt.audience)
        self.fields["objective"].setPlainText(self.prompt.objective)
        self.fields["branches"].setPlainText(self.prompt.branches)
        self.fields["evaluation"].setPlainText(self.prompt.evaluation)
        self.fields["format"].setText(self.prompt.format)
        self.fields["length"].setText(self.prompt.length)
    
    def update_prompt_from_fields(self):
        """Update prompt data from form fields."""
        if not isinstance(self.prompt, TreeOfThoughtsPrompt):
            self.prompt = TreeOfThoughtsPrompt()
        
        self.prompt.topic = self.fields["topic"].text()
        self.prompt.audience = self.fields["audience"].text()
        self.prompt.objective = self.fields["objective"].toPlainText()
        self.prompt.branches = self.fields["branches"].toPlainText()
        self.prompt.evaluation = self.fields["evaluation"].toPlainText()
        self.prompt.format = self.fields["format"].text()
        self.prompt.length = self.fields["length"].text()


class ActivePromptForm(BasePromptForm):
    """Form for Active Prompting."""
    
    def setup_ui(self):
        """Set up the UI components."""
        super().setup_ui()
        
        # Topic
        self.fields["topic"] = QLineEdit()
        self.layout.addRow("Topic:", self.fields["topic"])
        
        # Audience
        self.fields["audience"] = QLineEdit()
        self.layout.addRow("Audience:", self.fields["audience"])
        
        # Learning Objective
        self.fields["objective"] = QTextEdit()
        self.fields["objective"].setMaximumHeight(80)
        self.layout.addRow("Learning Objective:", self.fields["objective"])
        
        # Initial Question
        self.fields["initial_question"] = QTextEdit()
        self.fields["initial_question"].setMaximumHeight(80)
        self.layout.addRow("Initial Question:", self.fields["initial_question"])
        
        # Follow-up Prompts
        self.fields["followups"] = QTextEdit()
        self.layout.addRow("Follow-up Prompts:", self.fields["followups"])
        
        # Format
        self.fields["format"] = QLineEdit()
        self.layout.addRow("Format:", self.fields["format"])
        
        # Length
        self.fields["length"] = QLineEdit()
        self.layout.addRow("Length:", self.fields["length"])
    
    def connect_signals(self):
        """Connect signals to slots."""
        for field in self.fields.values():
            if isinstance(field, QLineEdit):
                field.textChanged.connect(self.field_changed)
            elif isinstance(field, QTextEdit):
                field.textChanged.connect(self.field_changed)
    
    def update_fields_from_prompt(self):
        """Update form fields from prompt data."""
        if not isinstance(self.prompt, ActivePrompt):
            return
        
        self.fields["topic"].setText(self.prompt.topic)
        self.fields["audience"].setText(self.prompt.audience)
        self.fields["objective"].setPlainText(self.prompt.objective)
        self.fields["initial_question"].setPlainText(self.prompt.initial_question)
        self.fields["followups"].setPlainText(self.prompt.followups)
        self.fields["format"].setText(self.prompt.format)
        self.fields["length"].setText(self.prompt.length)
    
    def update_prompt_from_fields(self):
        """Update prompt data from form fields."""
        if not isinstance(self.prompt, ActivePrompt):
            self.prompt = ActivePrompt()
        
        self.prompt.topic = self.fields["topic"].text()
        self.prompt.audience = self.fields["audience"].text()
        self.prompt.objective = self.fields["objective"].toPlainText()
        self.prompt.initial_question = self.fields["initial_question"].toPlainText()
        self.prompt.followups = self.fields["followups"].toPlainText()
        self.prompt.format = self.fields["format"].text()
        self.prompt.length = self.fields["length"].text()


class PersonaPromptForm(BasePromptForm):
    """Form for Persona-based Prompting."""
    
    def setup_ui(self):
        """Set up the UI components."""
        super().setup_ui()
        
        # Topic
        self.fields["topic"] = QLineEdit()
        self.layout.addRow("Topic:", self.fields["topic"])
        
        # Audience
        self.fields["audience"] = QLineEdit()
        self.layout.addRow("Audience:", self.fields["audience"])
        
        # Learning Objective
        self.fields["objective"] = QTextEdit()
        self.fields["objective"].setMaximumHeight(80)
        self.layout.addRow("Learning Objective:", self.fields["objective"])
        
        # Persona/Role
        self.fields["role"] = QLineEdit()
        self.layout.addRow("Persona/Role:", self.fields["role"])
        
        # Expertise Level
        self.fields["expertise"] = QComboBox()
        self.fields["expertise"].addItems(["Beginner", "Intermediate", "Expert", "World-class Expert"])
        self.layout.addRow("Expertise Level:", self.fields["expertise"])
        
        # Communication Style
        self.fields["style"] = QComboBox()
        self.fields["style"].addItems(["Academic", "Conversational", "Technical", "Simplified", "Socratic"])
        self.layout.addRow("Communication Style:", self.fields["style"])
        
        # Specific Knowledge
        self.fields["knowledge"] = QTextEdit()
        self.layout.addRow("Specific Knowledge:", self.fields["knowledge"])
        
        # Format
        self.fields["format"] = QLineEdit()
        self.layout.addRow("Format:", self.fields["format"])
        
        # Length
        self.fields["length"] = QLineEdit()
        self.layout.addRow("Length:", self.fields["length"])
    
    def connect_signals(self):
        """Connect signals to slots."""
        for field in self.fields.values():
            if isinstance(field, QLineEdit):
                field.textChanged.connect(self.field_changed)
            elif isinstance(field, QTextEdit):
                field.textChanged.connect(self.field_changed)
            elif isinstance(field, QComboBox):
                field.currentTextChanged.connect(self.field_changed)
    
    def update_fields_from_prompt(self):
        """Update form fields from prompt data."""
        if not isinstance(self.prompt, PersonaPrompt):
            return
        
        self.fields["topic"].setText(self.prompt.topic)
        self.fields["audience"].setText(self.prompt.audience)
        self.fields["objective"].setPlainText(self.prompt.objective)
        self.fields["role"].setText(self.prompt.role)
        
        # Set combo box values if they exist in the list
        expertise_index = self.fields["expertise"].findText(self.prompt.expertise)
        if expertise_index >= 0:
            self.fields["expertise"].setCurrentIndex(expertise_index)
        
        style_index = self.fields["style"].findText(self.prompt.style)
        if style_index >= 0:
            self.fields["style"].setCurrentIndex(style_index)
        
        self.fields["knowledge"].setPlainText(self.prompt.knowledge)
        self.fields["format"].setText(self.prompt.format)
        self.fields["length"].setText(self.prompt.length)
    
    def update_prompt_from_fields(self):
        """Update prompt data from form fields."""
        if not isinstance(self.prompt, PersonaPrompt):
            self.prompt = PersonaPrompt()
        
        self.prompt.topic = self.fields["topic"].text()
        self.prompt.audience = self.fields["audience"].text()
        self.prompt.objective = self.fields["objective"].toPlainText()
        self.prompt.role = self.fields["role"].text()
        self.prompt.expertise = self.fields["expertise"].currentText()
        self.prompt.style = self.fields["style"].currentText()
        self.prompt.knowledge = self.fields["knowledge"].toPlainText()
        self.prompt.format = self.fields["format"].text()
        self.prompt.length = self.fields["length"].text()
