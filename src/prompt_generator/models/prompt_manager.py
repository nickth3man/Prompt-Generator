"""
Prompt Manager for the Prompt Generator application.
Manages prompt history, templates, and storage.
"""

import os
import json
import shutil
from datetime import datetime
from typing import List, Dict, Any, Optional

from .prompt import BasePrompt, ChainOfThoughtPrompt, TreeOfThoughtsPrompt, ActivePrompt, PersonaPrompt


class PromptManager:
    """Manages prompt history, templates, and storage."""
    
    def __init__(self, base_dir=None):
        """Initialize the prompt manager."""
        if base_dir is None:
            # Use default location in user's home directory
            home_dir = os.path.expanduser("~")
            self.base_dir = os.path.join(home_dir, "PromptGenerator")
        else:
            self.base_dir = base_dir
        
        # Create directories if they don't exist
        self.prompts_dir = os.path.join(self.base_dir, "prompts")
        self.templates_dir = os.path.join(self.base_dir, "templates")
        self.history_dir = os.path.join(self.base_dir, "history")
        
        os.makedirs(self.prompts_dir, exist_ok=True)
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.history_dir, exist_ok=True)
        
        # Initialize prompt type mapping
        self.prompt_types = {
            "cot": ChainOfThoughtPrompt,
            "tot": TreeOfThoughtsPrompt,
            "active": ActivePrompt,
            "persona": PersonaPrompt
        }
    
    def create_prompt(self, prompt_type: str, title: str = "") -> Optional[BasePrompt]:
        """Create a new prompt of the specified type."""
        if prompt_type not in self.prompt_types:
            return None
        
        return self.prompt_types[prompt_type](title)
    
    def save_prompt(self, prompt: BasePrompt, as_template: bool = False) -> str:
        """Save a prompt to file."""
        if not prompt.title:
            # Generate a title if none exists
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            prompt.title = f"{prompt.type.upper()}_{timestamp}"
        
        # Update the updated_at timestamp
        prompt.updated_at = datetime.now()
        
        # Determine save directory
        save_dir = self.templates_dir if as_template else self.prompts_dir
        
        # Create a valid filename
        filename = f"{prompt.title.replace(' ', '_')}.json"
        filepath = os.path.join(save_dir, filename)
        
        # Save the prompt
        prompt.save(filepath)
        
        # Add to history if it's not a template
        if not as_template:
            self._add_to_history(prompt)
        
        return filepath
    
    def load_prompt(self, filename: str, from_template: bool = False) -> Optional[BasePrompt]:
        """Load a prompt from file."""
        # Determine load directory
        load_dir = self.templates_dir if from_template else self.prompts_dir
        
        filepath = os.path.join(load_dir, filename)
        
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            prompt_type = data.get("type")
            if prompt_type not in self.prompt_types:
                return None
            
            return self.prompt_types[prompt_type].from_dict(data)
        except Exception as e:
            print(f"Error loading prompt: {e}")
            return None
    
    def list_prompts(self, prompt_type: str = None) -> List[Dict[str, Any]]:
        """List all saved prompts, optionally filtered by type."""
        prompts = []
        
        for filename in os.listdir(self.prompts_dir):
            if not filename.endswith('.json'):
                continue
            
            filepath = os.path.join(self.prompts_dir, filename)
            
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                if prompt_type is None or data.get("type") == prompt_type:
                    prompts.append({
                        "filename": filename,
                        "title": data.get("title", ""),
                        "type": data.get("type", ""),
                        "created_at": data.get("created_at", ""),
                        "updated_at": data.get("updated_at", "")
                    })
            except Exception as e:
                print(f"Error reading prompt file {filename}: {e}")
        
        # Sort by updated_at (newest first)
        prompts.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        
        return prompts
    
    def list_templates(self, prompt_type: str = None) -> List[Dict[str, Any]]:
        """List all saved templates, optionally filtered by type."""
        templates = []
        
        for filename in os.listdir(self.templates_dir):
            if not filename.endswith('.json'):
                continue
            
            filepath = os.path.join(self.templates_dir, filename)
            
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                if prompt_type is None or data.get("type") == prompt_type:
                    templates.append({
                        "filename": filename,
                        "title": data.get("title", ""),
                        "type": data.get("type", ""),
                        "created_at": data.get("created_at", ""),
                        "updated_at": data.get("updated_at", "")
                    })
            except Exception as e:
                print(f"Error reading template file {filename}: {e}")
        
        # Sort by title
        templates.sort(key=lambda x: x.get("title", ""))
        
        return templates
    
    def delete_prompt(self, filename: str) -> bool:
        """Delete a prompt file."""
        filepath = os.path.join(self.prompts_dir, filename)
        
        if not os.path.exists(filepath):
            return False
        
        try:
            os.remove(filepath)
            return True
        except Exception as e:
            print(f"Error deleting prompt: {e}")
            return False
    
    def delete_template(self, filename: str) -> bool:
        """Delete a template file."""
        filepath = os.path.join(self.templates_dir, filename)
        
        if not os.path.exists(filepath):
            return False
        
        try:
            os.remove(filepath)
            return True
        except Exception as e:
            print(f"Error deleting template: {e}")
            return False
    
    def _add_to_history(self, prompt: BasePrompt) -> None:
        """Add a prompt to the history."""
        # Create a history entry
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        history_filename = f"{prompt.type}_{timestamp}.json"
        history_filepath = os.path.join(self.history_dir, history_filename)
        
        # Save a copy to history
        prompt.save(history_filepath)
        
        # Limit history size (keep the most recent N entries)
        self._prune_history(50)  # Keep the most recent 50 entries
    
    def _prune_history(self, max_entries: int) -> None:
        """Limit the history to the most recent entries."""
        history_files = []
        
        for filename in os.listdir(self.history_dir):
            if not filename.endswith('.json'):
                continue
            
            filepath = os.path.join(self.history_dir, filename)
            history_files.append((filepath, os.path.getmtime(filepath)))
        
        # Sort by modification time (newest first)
        history_files.sort(key=lambda x: x[1], reverse=True)
        
        # Remove excess files
        if len(history_files) > max_entries:
            for filepath, _ in history_files[max_entries:]:
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Error pruning history: {e}")
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the most recent prompt history entries."""
        history_entries = []
        
        for filename in os.listdir(self.history_dir):
            if not filename.endswith('.json'):
                continue
            
            filepath = os.path.join(self.history_dir, filename)
            
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                history_entries.append({
                    "filename": filename,
                    "title": data.get("title", ""),
                    "type": data.get("type", ""),
                    "created_at": data.get("created_at", ""),
                    "updated_at": data.get("updated_at", ""),
                    "content": data
                })
            except Exception as e:
                print(f"Error reading history file {filename}: {e}")
        
        # Sort by updated_at (newest first)
        history_entries.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        
        # Limit to the requested number
        return history_entries[:limit]
    
    def create_default_templates(self) -> None:
        """Create default templates for each prompt type."""
        # Chain of Thought template
        cot = ChainOfThoughtPrompt("Basic Chain of Thought")
        cot.topic = "[Your topic]"
        cot.audience = "[Target audience]"
        cot.objective = "[Learning objective]"
        cot.steps = "1. [First step]\n2. [Second step]\n3. [Third step]"
        cot.format = "[Format, e.g., 'article', 'lesson plan']"
        cot.length = "[Length, e.g., '500 words', '10 minutes']"
        self.save_prompt(cot, as_template=True)
        
        # Tree of Thoughts template
        tot = TreeOfThoughtsPrompt("Basic Tree of Thoughts")
        tot.topic = "[Your topic]"
        tot.audience = "[Target audience]"
        tot.objective = "[Learning objective]"
        tot.branches = "Branch 1: [First approach]\nBranch 2: [Second approach]\nBranch 3: [Third approach]"
        tot.evaluation = "[Criteria for evaluating each approach]"
        tot.format = "[Format, e.g., 'article', 'lesson plan']"
        tot.length = "[Length, e.g., '500 words', '10 minutes']"
        self.save_prompt(tot, as_template=True)
        
        # Active Prompting template
        active = ActivePrompt("Basic Active Prompting")
        active.topic = "[Your topic]"
        active.audience = "[Target audience]"
        active.objective = "[Learning objective]"
        active.initial_question = "[Initial question to start the learning process]"
        active.followups = "1. [First follow-up]\n2. [Second follow-up]\n3. [Third follow-up]"
        active.format = "[Format, e.g., 'article', 'lesson plan']"
        active.length = "[Length, e.g., '500 words', '10 minutes']"
        self.save_prompt(active, as_template=True)
        
        # Persona Prompting template
        persona = PersonaPrompt("Basic Persona Prompting")
        persona.topic = "[Your topic]"
        persona.audience = "[Target audience]"
        persona.objective = "[Learning objective]"
        persona.role = "[Role or persona]"
        persona.expertise = "[Expertise level]"
        persona.style = "[Communication style]"
        persona.knowledge = "[Specific knowledge or expertise]"
        persona.format = "[Format, e.g., 'article', 'lesson plan']"
        persona.length = "[Length, e.g., '500 words', '10 minutes']"
        self.save_prompt(persona, as_template=True)
