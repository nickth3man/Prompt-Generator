"""
Prompt models for the Prompt Generator application.
Defines data structures for different prompt types.
"""

import json
import os
from datetime import datetime


class BasePrompt:
    """Base class for all prompt types."""
    
    def __init__(self, title="", prompt_type=""):
        self.title = title
        self.type = prompt_type
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self):
        """Convert prompt to dictionary."""
        return {
            "title": self.title,
            "type": self.type,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create prompt from dictionary."""
        prompt = cls()
        prompt.title = data.get("title", "")
        prompt.type = data.get("type", "")
        
        # Parse dates if they exist
        created_at = data.get("created_at")
        if created_at:
            try:
                prompt.created_at = datetime.fromisoformat(created_at)
            except (ValueError, TypeError):
                prompt.created_at = datetime.now()
        
        updated_at = data.get("updated_at")
        if updated_at:
            try:
                prompt.updated_at = datetime.fromisoformat(updated_at)
            except (ValueError, TypeError):
                prompt.updated_at = datetime.now()
        
        return prompt
    
    def save(self, filepath):
        """Save prompt to file."""
        data = self.to_dict()
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)
    
    @classmethod
    def load(cls, filepath):
        """Load prompt from file."""
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            return cls.from_dict(data)
        except Exception as e:
            print(f"Error loading prompt: {e}")
            return None
    
    def generate_text(self):
        """Generate prompt text. To be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method")


class ChainOfThoughtPrompt(BasePrompt):
    """Chain of Thought prompt model."""
    
    def __init__(self, title=""):
        super().__init__(title, "cot")
        self.topic = ""
        self.audience = ""
        self.objective = ""
        self.steps = ""
        self.format = ""
        self.length = ""
    
    def to_dict(self):
        """Convert prompt to dictionary."""
        data = super().to_dict()
        data.update({
            "topic": self.topic,
            "audience": self.audience,
            "objective": self.objective,
            "steps": self.steps,
            "format": self.format,
            "length": self.length
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create prompt from dictionary."""
        prompt = super(ChainOfThoughtPrompt, cls).from_dict(data)
        prompt.topic = data.get("topic", "")
        prompt.audience = data.get("audience", "")
        prompt.objective = data.get("objective", "")
        prompt.steps = data.get("steps", "")
        prompt.format = data.get("format", "")
        prompt.length = data.get("length", "")
        return prompt
    
    def generate_text(self):
        """Generate prompt text."""
        return (
            f"Topic: {self.topic}\n\n"
            f"For {self.audience}, I need a detailed explanation on {self.topic} that achieves the following learning objective:\n"
            f"{self.objective}\n\n"
            f"Please use a Chain-of-Thought approach to break down this topic into the following logical steps:\n"
            f"{self.steps}\n\n"
            f"The content should be in {self.format} format and approximately {self.length} in length."
        )


class TreeOfThoughtsPrompt(BasePrompt):
    """Tree of Thoughts prompt model."""
    
    def __init__(self, title=""):
        super().__init__(title, "tot")
        self.topic = ""
        self.audience = ""
        self.objective = ""
        self.branches = ""
        self.evaluation = ""
        self.format = ""
        self.length = ""
    
    def to_dict(self):
        """Convert prompt to dictionary."""
        data = super().to_dict()
        data.update({
            "topic": self.topic,
            "audience": self.audience,
            "objective": self.objective,
            "branches": self.branches,
            "evaluation": self.evaluation,
            "format": self.format,
            "length": self.length
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create prompt from dictionary."""
        prompt = super(TreeOfThoughtsPrompt, cls).from_dict(data)
        prompt.topic = data.get("topic", "")
        prompt.audience = data.get("audience", "")
        prompt.objective = data.get("objective", "")
        prompt.branches = data.get("branches", "")
        prompt.evaluation = data.get("evaluation", "")
        prompt.format = data.get("format", "")
        prompt.length = data.get("length", "")
        return prompt
    
    def generate_text(self):
        """Generate prompt text."""
        return (
            f"Topic: {self.topic}\n\n"
            f"For {self.audience}, I need an exploration of {self.topic} that achieves the following learning objective:\n"
            f"{self.objective}\n\n"
            f"Please use a Tree-of-Thoughts approach to explore these different solution paths:\n"
            f"{self.branches}\n\n"
            f"Evaluate each path using these criteria:\n"
            f"{self.evaluation}\n\n"
            f"The content should be in {self.format} format and approximately {self.length} in length."
        )


class ActivePrompt(BasePrompt):
    """Active Prompting model."""
    
    def __init__(self, title=""):
        super().__init__(title, "active")
        self.topic = ""
        self.audience = ""
        self.objective = ""
        self.initial_question = ""
        self.followups = ""
        self.format = ""
        self.length = ""
    
    def to_dict(self):
        """Convert prompt to dictionary."""
        data = super().to_dict()
        data.update({
            "topic": self.topic,
            "audience": self.audience,
            "objective": self.objective,
            "initial_question": self.initial_question,
            "followups": self.followups,
            "format": self.format,
            "length": self.length
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create prompt from dictionary."""
        prompt = super(ActivePrompt, cls).from_dict(data)
        prompt.topic = data.get("topic", "")
        prompt.audience = data.get("audience", "")
        prompt.objective = data.get("objective", "")
        prompt.initial_question = data.get("initial_question", "")
        prompt.followups = data.get("followups", "")
        prompt.format = data.get("format", "")
        prompt.length = data.get("length", "")
        return prompt
    
    def generate_text(self):
        """Generate prompt text."""
        return (
            f"Topic: {self.topic}\n\n"
            f"For {self.audience}, I need an interactive learning experience on {self.topic} that achieves the following learning objective:\n"
            f"{self.objective}\n\n"
            f"Begin with this initial question:\n"
            f"{self.initial_question}\n\n"
            f"Then use these follow-up prompts to guide the learning process:\n"
            f"{self.followups}\n\n"
            f"The content should be in {self.format} format and approximately {self.length} in length."
        )


class PersonaPrompt(BasePrompt):
    """Persona-based Prompting model."""
    
    def __init__(self, title=""):
        super().__init__(title, "persona")
        self.topic = ""
        self.audience = ""
        self.objective = ""
        self.role = ""
        self.expertise = ""
        self.style = ""
        self.knowledge = ""
        self.format = ""
        self.length = ""
    
    def to_dict(self):
        """Convert prompt to dictionary."""
        data = super().to_dict()
        data.update({
            "topic": self.topic,
            "audience": self.audience,
            "objective": self.objective,
            "role": self.role,
            "expertise": self.expertise,
            "style": self.style,
            "knowledge": self.knowledge,
            "format": self.format,
            "length": self.length
        })
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create prompt from dictionary."""
        prompt = super(PersonaPrompt, cls).from_dict(data)
        prompt.topic = data.get("topic", "")
        prompt.audience = data.get("audience", "")
        prompt.objective = data.get("objective", "")
        prompt.role = data.get("role", "")
        prompt.expertise = data.get("expertise", "")
        prompt.style = data.get("style", "")
        prompt.knowledge = data.get("knowledge", "")
        prompt.format = data.get("format", "")
        prompt.length = data.get("length", "")
        return prompt
    
    def generate_text(self):
        """Generate prompt text."""
        return (
            f"Topic: {self.topic}\n\n"
            f"For {self.audience}, I need content on {self.topic} that achieves the following learning objective:\n"
            f"{self.objective}\n\n"
            f"Please respond as if you are a {self.expertise} {self.role} with the following specific knowledge:\n"
            f"{self.knowledge}\n\n"
            f"Use a {self.style} communication style.\n\n"
            f"The content should be in {self.format} format and approximately {self.length} in length."
        )
