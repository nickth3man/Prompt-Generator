import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QComboBox, QStackedWidget, QPushButton, QTextEdit, 
                            QLineEdit, QFormLayout, QGroupBox, QSplitter, QFrame, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import json
import os

class PromptGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Advanced Prompt Generator for L&D Professionals")
        self.setMinimumSize(1000, 700)
        
        # Main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Header
        self.setup_header()
        
        # Content splitter
        self.splitter = QSplitter(Qt.Horizontal)
        
        # Setup category selection sidebar
        self.setup_sidebar()
        
        # Setup main content area
        self.setup_content_area()
        
        # Add to splitter
        self.splitter.addWidget(self.sidebar_widget)
        self.splitter.addWidget(self.content_widget)
        self.splitter.setSizes([200, 800])
        
        # Add splitter to main layout
        self.main_layout.addWidget(self.splitter)
        
        # Footer with buttons
        self.setup_footer()
        
        # Initialize data
        self.current_prompt_data = {}
        self.initialize_prompt_templates()

    def setup_header(self):
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        
        title_label = QLabel("Advanced Prompt Generator")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        self.main_layout.addWidget(header_widget)

    def setup_sidebar(self):
        self.sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(self.sidebar_widget)
        
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
            button.clicked.connect(self.select_category)
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
    
    def setup_content_area(self):
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        
        # Welcome screen
        self.welcome_widget = QWidget()
        welcome_layout = QVBoxLayout(self.welcome_widget)
        
        welcome_title = QLabel("Welcome to the Advanced Prompt Generator")
        welcome_title.setFont(QFont("Arial", 14, QFont.Bold))
        welcome_description = QLabel(
            "This tool will help you create effective prompts for AI-assisted content creation.\n\n"
            "Choose a prompt category from the left sidebar to get started:\n"
            "• Chain-of-Thought (CoT): Break complex topics into logical sequential steps\n"
            "• Tree-of-Thoughts (ToT): Explore multiple solution paths simultaneously\n"
            "• Active Prompting: Utilize iterative refinement based on feedback\n"
            "• Persona-based Prompting: Leverage role assumption for specialized expertise\n\n"
            "Each generator will guide you through creating a prompt optimized for your L&D needs."
        )
        welcome_description.setWordWrap(True)
        
        welcome_layout.addWidget(welcome_title)
        welcome_layout.addWidget(welcome_description)
        welcome_layout.addStretch()
        
        # Stacked widget for different prompt builders
        self.prompt_stack = QStackedWidget()
        self.prompt_stack.addWidget(self.welcome_widget)
        
        # Create prompt builder widgets
        self.setup_cot_builder()
        self.setup_tot_builder()
        self.setup_active_builder()
        self.setup_persona_builder()
        
        # Add to content area
        self.content_layout.addWidget(self.prompt_stack)
        
        # Preview area
        self.setup_preview_area()
        
    def setup_preview_area(self):
        preview_group = QGroupBox("Prompt Preview")
        preview_layout = QVBoxLayout()
        
        self.preview_text = QTextEdit()
        self.preview_text.setReadOnly(True)
        self.preview_text.setMinimumHeight(200)
        
        preview_layout.addWidget(self.preview_text)
        preview_group.setLayout(preview_layout)
        
        self.content_layout.addWidget(preview_group)
    
    def setup_cot_builder(self):
        self.cot_widget = QWidget()
        form_layout = QFormLayout(self.cot_widget)
        
        self.cot_fields = {}
        
        # Topic
        self.cot_fields["topic"] = QLineEdit()
        form_layout.addRow("Topic:", self.cot_fields["topic"])
        
        # Audience
        self.cot_fields["audience"] = QLineEdit()
        form_layout.addRow("Audience:", self.cot_fields["audience"])
        
        # Learning Objective
        self.cot_fields["objective"] = QTextEdit()
        self.cot_fields["objective"].setMaximumHeight(80)
        form_layout.addRow("Learning Objective:", self.cot_fields["objective"])
        
        # Reasoning Steps
        self.cot_fields["steps"] = QTextEdit()
        form_layout.addRow("Reasoning Steps:", self.cot_fields["steps"])
        
        # Format
        self.cot_fields["format"] = QLineEdit()
        form_layout.addRow("Format:", self.cot_fields["format"])
        
        # Length
        self.cot_fields["length"] = QLineEdit()
        form_layout.addRow("Length:", self.cot_fields["length"])
        
        # Connect signals
        for field in self.cot_fields.values():
            if isinstance(field, QLineEdit):
                field.textChanged.connect(self.update_cot_preview)
            elif isinstance(field, QTextEdit):
                field.textChanged.connect(self.update_cot_preview)
        
        self.prompt_stack.addWidget(self.cot_widget)
    
    def setup_tot_builder(self):
        self.tot_widget = QWidget()
        form_layout = QFormLayout(self.tot_widget)
        
        self.tot_fields = {}
        
        # Topic
        self.tot_fields["topic"] = QLineEdit()
        form_layout.addRow("Topic:", self.tot_fields["topic"])
        
        # Audience
        self.tot_fields["audience"] = QLineEdit()
        form_layout.addRow("Audience:", self.tot_fields["audience"])
        
        # Learning Objective
        self.tot_fields["objective"] = QTextEdit()
        self.tot_fields["objective"].setMaximumHeight(80)
        form_layout.addRow("Learning Objective:", self.tot_fields["objective"])
        
        # Thought Branches
        self.tot_fields["branches"] = QTextEdit()
        form_layout.addRow("Thought Branches:", self.tot_fields["branches"])
        
        # Evaluation Criteria
        self.tot_fields["evaluation"] = QTextEdit()
        self.tot_fields["evaluation"].setMaximumHeight(80)
        form_layout.addRow("Evaluation Criteria:", self.tot_fields["evaluation"])
        
        # Format
        self.tot_fields["format"] = QLineEdit()
        form_layout.addRow("Format:", self.tot_fields["format"])
        
        # Length
        self.tot_fields["length"] = QLineEdit()
        form_layout.addRow("Length:", self.tot_fields["length"])
        
        # Connect signals
        for field in self.tot_fields.values():
            if isinstance(field, QLineEdit):
                field.textChanged.connect(self.update_tot_preview)
            elif isinstance(field, QTextEdit):
                field.textChanged.connect(self.update_tot_preview)
        
        self.prompt_stack.addWidget(self.tot_widget)
    
    def setup_active_builder(self):
        self.active_widget = QWidget()
        form_layout = QFormLayout(self.active_widget)
        
        self.active_fields = {}
        
        # Topic
        self.active_fields["topic"] = QLineEdit()
        form_layout.addRow("Topic:", self.active_fields["topic"])
        
        # Audience
        self.active_fields["audience"] = QLineEdit()
        form_layout.addRow("Audience:", self.active_fields["audience"])
        
        # Learning Objective
        self.active_fields["objective"] = QTextEdit()
        self.active_fields["objective"].setMaximumHeight(80)
        form_layout.addRow("Learning Objective:", self.active_fields["objective"])
        
        # Initial Question
        self.active_fields["initial_question"] = QTextEdit()
        self.active_fields["initial_question"].setMaximumHeight(80)
        form_layout.addRow("Initial Question:", self.active_fields["initial_question"])
        
        # Follow-up Prompts
        self.active_fields["followups"] = QTextEdit()
        form_layout.addRow("Follow-up Prompts:", self.active_fields["followups"])
        
        # Format
        self.active_fields["format"] = QLineEdit()
        form_layout.addRow("Format:", self.active_fields["format"])
        
        # Length
        self.active_fields["length"] = QLineEdit()
        form_layout.addRow("Length:", self.active_fields["length"])
        
        # Connect signals
        for field in self.active_fields.values():
            if isinstance(field, QLineEdit):
                field.textChanged.connect(self.update_active_preview)
            elif isinstance(field, QTextEdit):
                field.textChanged.connect(self.update_active_preview)
        
        self.prompt_stack.addWidget(self.active_widget)
    
    def setup_persona_builder(self):
        self.persona_widget = QWidget()
        form_layout = QFormLayout(self.persona_widget)
        
        self.persona_fields = {}
        
        # Topic
        self.persona_fields["topic"] = QLineEdit()
        form_layout.addRow("Topic:", self.persona_fields["topic"])
        
        # Audience
        self.persona_fields["audience"] = QLineEdit()
        form_layout.addRow("Audience:", self.persona_fields["audience"])
        
        # Learning Objective
        self.persona_fields["objective"] = QTextEdit()
        self.persona_fields["objective"].setMaximumHeight(80)
        form_layout.addRow("Learning Objective:", self.persona_fields["objective"])
        
        # Persona/Role
        self.persona_fields["role"] = QLineEdit()
        form_layout.addRow("Persona/Role:", self.persona_fields["role"])
        
        # Expertise Level
        self.persona_fields["expertise"] = QComboBox()
        self.persona_fields["expertise"].addItems(["Beginner", "Intermediate", "Expert", "World-class Expert"])
        form_layout.addRow("Expertise Level:", self.persona_fields["expertise"])
        
        # Communication Style
        self.persona_fields["style"] = QComboBox()
        self.persona_fields["style"].addItems(["Academic", "Conversational", "Technical", "Simplified", "Socratic"])
        form_layout.addRow("Communication Style:", self.persona_fields["style"])
        
        # Specific Knowledge
        self.persona_fields["knowledge"] = QTextEdit()
        form_layout.addRow("Specific Knowledge:", self.persona_fields["knowledge"])
        
        # Format
        self.persona_fields["format"] = QLineEdit()
        form_layout.addRow("Format:", self.persona_fields["format"])
        
        # Length
        self.persona_fields["length"] = QLineEdit()
        form_layout.addRow("Length:", self.persona_fields["length"])
        
        # Connect signals
        for field in self.persona_fields.values():
            if isinstance(field, QLineEdit):
                field.textChanged.connect(self.update_persona_preview)
            elif isinstance(field, QTextEdit):
                field.textChanged.connect(self.update_persona_preview)
            elif isinstance(field, QComboBox):
                field.currentTextChanged.connect(self.update_persona_preview)
        
        self.prompt_stack.addWidget(self.persona_widget)

    def setup_footer(self):
        footer_widget = QWidget()
        footer_layout = QHBoxLayout(footer_widget)
        
        # Buttons
        self.save_button = QPushButton("Save Prompt")
        self.save_button.clicked.connect(self.save_prompt)
        
        self.copy_button = QPushButton("Copy to Clipboard")
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        
        self.clear_button = QPushButton("Clear Fields")
        self.clear_button.clicked.connect(self.clear_fields)
        
        footer_layout.addWidget(self.save_button)
        footer_layout.addWidget(self.copy_button)
        footer_layout.addWidget(self.clear_button)
        
        self.main_layout.addWidget(footer_widget)
    
    def initialize_prompt_templates(self):
        # Templates for each prompt type
        self.templates = {
            "cot": (
                "Topic: {topic}\n\n"
                "For {audience}, I need a detailed explanation on {topic} that achieves the following learning objective:\n"
                "{objective}\n\n"
                "Please use a Chain-of-Thought approach to break down this topic into the following logical steps:\n"
                "{steps}\n\n"
                "The content should be in {format} format and approximately {length} in length."
            ),
            "tot": (
                "Topic: {topic}\n\n"
                "For {audience}, I need an exploration of {topic} that achieves the following learning objective:\n"
                "{objective}\n\n"
                "Please use a Tree-of-Thoughts approach to explore these different solution paths:\n"
                "{branches}\n\n"
                "Evaluate each path using these criteria:\n"
                "{evaluation}\n\n"
                "The content should be in {format} format and approximately {length} in length."
            ),
            "active": (
                "Topic: {topic}\n\n"
                "For {audience}, I need an interactive learning experience on {topic} that achieves the following learning objective:\n"
                "{objective}\n\n"
                "Begin with this initial question:\n"
                "{initial_question}\n\n"
                "Then use these follow-up prompts to guide the learning process:\n"
                "{followups}\n\n"
                "The content should be in {format} format and approximately {length} in length."
            ),
            "persona": (
                "Topic: {topic}\n\n"
                "For {audience}, I need content on {topic} that achieves the following learning objective:\n"
                "{objective}\n\n"
                "Please respond as if you are a {expertise} {role} with the following specific knowledge:\n"
                "{knowledge}\n\n"
                "Use a {style} communication style.\n\n"
                "The content should be in {format} format and approximately {length} in length."
            )
        }
    
    def select_category(self):
        sender = self.sender()
        category = sender.property("category")
        
        # Highlight selected button
        for button in self.category_buttons:
            button.setStyleSheet("")
        sender.setStyleSheet("background-color: #e0e0e0;")
        
        # Show corresponding prompt builder
        if category == "cot":
            self.prompt_stack.setCurrentWidget(self.cot_widget)
            self.current_prompt_data = {"type": "cot"}
        elif category == "tot":
            self.prompt_stack.setCurrentWidget(self.tot_widget)
            self.current_prompt_data = {"type": "tot"}
        elif category == "active":
            self.prompt_stack.setCurrentWidget(self.active_widget)
            self.current_prompt_data = {"type": "active"}
        elif category == "persona":
            self.prompt_stack.setCurrentWidget(self.persona_widget)
            self.current_prompt_data = {"type": "persona"}
    
    def update_cot_preview(self):
        # Gather data from form fields
        data = {
            "topic": self.cot_fields["topic"].text(),
            "audience": self.cot_fields["audience"].text(),
            "objective": self.cot_fields["objective"].toPlainText(),
            "steps": self.cot_fields["steps"].toPlainText(),
            "format": self.cot_fields["format"].text(),
            "length": self.cot_fields["length"].text()
        }
        
        # Update current data
        self.current_prompt_data.update(data)
        
        # Generate preview
        preview = self.templates["cot"].format(**data)
        self.preview_text.setText(preview)
    
    def update_tot_preview(self):
        # Gather data from form fields
        data = {
            "topic": self.tot_fields["topic"].text(),
            "audience": self.tot_fields["audience"].text(),
            "objective": self.tot_fields["objective"].toPlainText(),
            "branches": self.tot_fields["branches"].toPlainText(),
            "evaluation": self.tot_fields["evaluation"].toPlainText(),
            "format": self.tot_fields["format"].text(),
            "length": self.tot_fields["length"].text()
        }
        
        # Update current data
        self.current_prompt_data.update(data)
        
        # Generate preview
        preview = self.templates["tot"].format(**data)
        self.preview_text.setText(preview)
    
    def update_active_preview(self):
        # Gather data from form fields
        data = {
            "topic": self.active_fields["topic"].text(),
            "audience": self.active_fields["audience"].text(),
            "objective": self.active_fields["objective"].toPlainText(),
            "initial_question": self.active_fields["initial_question"].toPlainText(),
            "followups": self.active_fields["followups"].toPlainText(),
            "format": self.active_fields["format"].text(),
            "length": self.active_fields["length"].text()
        }
        
        # Update current data
        self.current_prompt_data.update(data)
        
        # Generate preview
        preview = self.templates["active"].format(**data)
        self.preview_text.setText(preview)
    
    def update_persona_preview(self):
        # Gather data from form fields
        data = {
            "topic": self.persona_fields["topic"].text(),
            "audience": self.persona_fields["audience"].text(),
            "objective": self.persona_fields["objective"].toPlainText(),
            "role": self.persona_fields["role"].text(),
            "expertise": self.persona_fields["expertise"].currentText(),
            "style": self.persona_fields["style"].currentText(),
            "knowledge": self.persona_fields["knowledge"].toPlainText(),
            "format": self.persona_fields["format"].text(),
            "length": self.persona_fields["length"].text()
        }
        
        # Update current data
        self.current_prompt_data.update(data)
        
        # Generate preview
        preview = self.templates["persona"].format(**data)
        self.preview_text.setText(preview)
    
    def save_prompt(self):
        if not self.current_prompt_data:
            return
        
        # Open file dialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Prompt", "", "JSON Files (*.json);;All Files (*)"
        )
        
        if not file_path:
            return
        
        # Add file extension if not provided
        if not file_path.endswith('.json'):
            file_path += '.json'
        
        # Save to file
        with open(file_path, 'w') as f:
            json.dump(self.current_prompt_data, f, indent=4)
    
    def copy_to_clipboard(self):
        # Copy preview text to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(self.preview_text.toPlainText())
    
    def clear_fields(self):
        # Clear fields based on current prompt type
        prompt_type = self.current_prompt_data.get("type")
        
        if prompt_type == "cot":
            for field in self.cot_fields.values():
                if isinstance(field, QLineEdit):
                    field.clear()
                elif isinstance(field, QTextEdit):
                    field.clear()
        elif prompt_type == "tot":
            for field in self.tot_fields.values():
                if isinstance(field, QLineEdit):
                    field.clear()
                elif isinstance(field, QTextEdit):
                    field.clear()
        elif prompt_type == "active":
            for field in self.active_fields.values():
                if isinstance(field, QLineEdit):
                    field.clear()
                elif isinstance(field, QTextEdit):
                    field.clear()
        elif prompt_type == "persona":
            for field in self.persona_fields.values():
                if isinstance(field, QLineEdit):
                    field.clear()
                elif isinstance(field, QTextEdit):
                    field.clear()
                elif isinstance(field, QComboBox):
                    field.setCurrentIndex(0)
        
        # Clear preview
        self.preview_text.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PromptGeneratorApp()
    window.show()
    sys.exit(app.exec_())
