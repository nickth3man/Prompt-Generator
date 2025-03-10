# Advanced Prompt Generator for L&D Professionals

A PyQt5-based application for creating different types of educational prompts to enhance learning and development activities.

## Features

- Create four types of specialized prompts:
  - **Chain-of-Thought (CoT)**: Break complex topics into logical sequential steps
  - **Tree-of-Thoughts (ToT)**: Explore multiple solution paths simultaneously
  - **Active Prompting**: Utilize iterative refinement based on feedback
  - **Persona-based Prompting**: Leverage role assumption for specialized expertise

- User-friendly interface with:
  - Category selection sidebar
  - Specialized forms for each prompt type
  - Real-time prompt preview
  - Save, load, and export functionality

## Installation

### Prerequisites

- Python 3.6 or higher
- PyQt5 5.15.0 or higher

### Option 1: Install from source

1. Clone the repository:
   ```
   git clone <repository-url>
   cd "Prompt Generator"
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install the package in development mode:
   ```
   pip install -e .
   ```

### Option 2: Install dependencies only

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

After installation, you can run the application using one of the following methods:

1. Using the entry point (if installed with `pip install -e .`):
   ```
   prompt_generator
   ```

2. Using the main script:
   ```
   python main.py
   ```

### Creating a Prompt

1. Select a prompt type from the sidebar
2. Fill in the form fields
3. View the generated prompt in the preview area
4. Save or export the prompt as needed

## Project Structure

```
Prompt Generator/
├── main.py                      # Main entry point
├── setup.py                     # Package installation script
├── requirements.txt             # Dependencies
├── README.md                    # This file
├── app_icon.ico                 # Application icon
├── src/
│   └── prompt_generator/        # Main package
│       ├── __init__.py          # Package initialization
│       ├── app.py               # Main application module
│       ├── models/              # Data models
│       │   ├── __init__.py
│       │   ├── prompt.py        # Prompt models
│       │   └── prompt_manager.py # Prompt management
│       ├── ui/                  # UI components
│       │   ├── __init__.py
│       │   ├── content.py       # Main content area
│       │   ├── footer.py        # Footer with buttons
│       │   ├── header.py        # Application header
│       │   ├── preview.py       # Prompt preview
│       │   ├── prompt_forms.py  # Forms for different prompts
│       │   ├── sidebar.py       # Category selection sidebar
│       │   └── welcome.py       # Welcome screen
│       ├── utils/               # Utility functions
│       │   ├── __init__.py
│       │   ├── settings.py      # Settings management
│       │   └── stylesheets.py   # UI styling
│       └── resources/           # Application resources
```

## Development

### Running Tests

```
# To be implemented
```

### Building an Executable

To build a standalone executable:

```
pyinstaller main.py --name "Prompt Generator" --windowed --icon=app_icon.ico
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- PyQt5 for the GUI framework
- All contributors to the project
