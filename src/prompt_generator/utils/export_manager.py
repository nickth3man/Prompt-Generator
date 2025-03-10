"""
Export management for the Prompt Generator application.
Provides functionality for exporting prompts to different formats.
"""

import os
import json
from .settings import Settings


class ExportManager:
    """Manages prompt exports to different formats."""

    def __init__(self):
        """Initialize the export manager."""
        self.settings = Settings()
        self.supported_formats = self.settings.get("export_formats")

    def export_prompt(self, prompt_data, filepath, format_type=None):
        """Export a prompt to a file.

        Args:
            prompt_data: Dictionary containing prompt data
            filepath: Path to save the exported file
            format_type: Format to export to (txt, md, html, json)

        Returns:
            True if successful, False otherwise
        """
        # If format not specified, try to determine from filepath extension
        if not format_type:
            _, ext = os.path.splitext(filepath)
            format_type = ext.lstrip('.').lower()

            # Default to txt if format not recognized
            if format_type not in self.supported_formats:
                format_type = self.settings.get("default_export_format")

        # Ensure filepath has the correct extension
        if not filepath.lower().endswith(f".{format_type}"):
            filepath = f"{filepath}.{format_type}"

        # Export based on format
        try:
            if format_type == "json":
                return self._export_json(prompt_data, filepath)
            elif format_type == "md":
                return self._export_markdown(prompt_data, filepath)
            elif format_type == "html":
                return self._export_html(prompt_data, filepath)
            else:  # Default to txt
                return self._export_text(prompt_data, filepath)
        except Exception as e:
            print(f"Error exporting prompt: {e}")
            return False

    def _export_text(self, prompt_data, filepath):
        """Export prompt as plain text.

        Args:
            prompt_data: Dictionary containing prompt data
            filepath: Path to save the exported file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get the generated text from the prompt data
            if "generated_text" in prompt_data:
                text = prompt_data["generated_text"]
            else:
                # Try to generate text if prompt object has generate_text method
                text = self._get_prompt_text(prompt_data)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            return True
        except Exception as e:
            print(f"Error exporting text: {e}")
            return False

    def _export_json(self, prompt_data, filepath):
        """Export prompt as JSON.

        Args:
            prompt_data: Dictionary containing prompt data
            filepath: Path to save the exported file

        Returns:
            True if successful, False otherwise
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(prompt_data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error exporting JSON: {e}")
            return False

    def _export_markdown(self, prompt_data, filepath):
        """Export prompt as Markdown.

        Args:
            prompt_data: Dictionary containing prompt data
            filepath: Path to save the exported file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get the generated text from the prompt data
            if "generated_text" in prompt_data:
                text = prompt_data["generated_text"]
            else:
                # Try to generate text if prompt object has generate_text method
                text = self._get_prompt_text(prompt_data)

            # Create markdown content
            title = prompt_data.get("title", "Untitled Prompt")
            prompt_type = prompt_data.get("type", "").upper()

            md_content = f"# {title}\n\n"
            md_content += f"**Type:** {prompt_type}\n\n"

            # Add metadata
            if "created_at" in prompt_data:
                md_content += f"**Created:** {prompt_data['created_at']}\n\n"

            # Add prompt text
            md_content += "## Prompt\n\n"
            md_content += text

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md_content)
            return True
        except Exception as e:
            print(f"Error exporting Markdown: {e}")
            return False

    def _export_html(self, prompt_data, filepath):
        """Export prompt as HTML.

        Args:
            prompt_data: Dictionary containing prompt data
            filepath: Path to save the exported file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get the generated text from the prompt data
            if "generated_text" in prompt_data:
                text = prompt_data["generated_text"]
            else:
                # Try to generate text if prompt object has generate_text method
                text = self._get_prompt_text(prompt_data)

            # Create HTML content
            title = prompt_data.get("title", "Untitled Prompt")
            prompt_type = prompt_data.get("type", "").upper()

            # Format text with paragraphs
            formatted_text = ""
            for line in text.split('\n'):
                if line.strip():
                    formatted_text += f"<p>{line}</p>\n"
                else:
                    formatted_text += "<br>\n"

            # Build HTML content in parts to avoid long lines
            html_start = (
                f"<!DOCTYPE html>\n"
                f"<html>\n"
                f"<head>\n"
                f"    <meta charset='UTF-8'>\n"
                f"    <meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
            )
            
            html_title = f"    <title>{title}</title>\n"
            
            style_start = (
                f"    <style>\n"
                f"        body {{\n"
                f"            font-family: Arial, sans-serif;\n"
                f"            line-height: 1.6;\n"
                f"            margin: 0;\n"
                f"            padding: 20px;\n"
                f"            color: #333;\n"
                f"        }}\n"
            )
            
            style_container = (
                f"        .container {{\n"
                f"            max-width: 800px;\n"
                f"            margin: 0 auto;\n"
                f"            background: #fff;\n"
                f"            padding: 20px;\n"
                f"            border-radius: 5px;\n"
                f"            box-shadow: 0 0 10px rgba(0,0,0,0.1);\n"
                f"        }}\n"
            )
            
            style_h1 = (
                f"        h1 {{\n"
                f"            color: #2c3e50;\n"
                f"            border-bottom: 2px solid #eee;\n"
                f"            padding-bottom: 10px;\n"
                f"        }}\n"
            )
            
            style_meta = (
                f"        .meta {{\n"
                f"            color: #7f8c8d;\n"
                f"            font-size: 0.9em;\n"
                f"            margin-bottom: 20px;\n"
                f"        }}\n"
            )
            
            style_prompt = (
                f"        .prompt-text {{\n"
                f"            background: #f9f9f9;\n"
                f"            padding: 15px;\n"
                f"            border-left: 4px solid #2c3e50;\n"
                f"            margin-bottom: 20px;\n"
                f"        }}\n"
                f"    </style>\n"
                f"</head>\n"
            )
            
            body_start = (
                f"<body>\n"
                f"    <div class='container'>\n"
                f"        <h1>{title}</h1>\n"
                f"        <div class='meta'>\n"
                f"            <strong>Type:</strong> {prompt_type}<br>\n"
            )
            
            # Combine all parts
            html_content = (
                html_start + html_title + style_start + 
                style_container + style_h1 + style_meta + 
                style_prompt + body_start
            )
            
            # Add creation date if available
            if "created_at" in prompt_data:
                created_at = prompt_data['created_at']
                created_line = (
                    f"            <strong>Created:</strong> "
                    f"{created_at}<br>\n"
                )
                html_content += created_line

            body_end = (
                f"        </div>\n"
                f"        <h2>Prompt</h2>\n"
                f"        <div class='prompt-text'>\n"
                f"{formatted_text}"
                f"        </div>\n"
                f"    </div>\n"
                f"</body>\n"
                f"</html>\n"
            )
            
            html_content += body_end

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            return True
        except Exception as e:
            print(f"Error exporting HTML: {e}")
            return False

    def _get_prompt_text(self, prompt_data):
        """Try to get generated text from prompt data.

        Args:
            prompt_data: Dictionary containing prompt data

        Returns:
            Generated text if available, otherwise a summary of prompt data
        """
        # If prompt data has a generate_text method, use it
        has_generate = hasattr(prompt_data, 'generate_text')
        is_callable = callable(getattr(prompt_data, 'generate_text', None))
        
        if has_generate and is_callable:
            return prompt_data.generate_text()

        # Otherwise, create a summary from the prompt data
        text = f"Title: {prompt_data.get('title', 'Untitled')}\n\n"

        # Add other fields
        excluded_keys = ['title', 'type', 'created_at', 'updated_at', 'id']
        for key, value in prompt_data.items():
            if key not in excluded_keys and value:
                text += f"{key.replace('_', ' ').title()}: {value}\n\n"

        return text
