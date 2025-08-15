#!/usr/bin/env python3
"""
Data Assistant Project - Streamlit Cloud Entry Point
This is the main entry point that Streamlit Cloud will use.
"""

import sys
from pathlib import Path

# Setup path einmal am Anfang
current_file = Path(__file__).resolve()
project_dir = current_file / "new_data_assistant_project"

# Add the project root to sys.path for imports
if str(current_file.parent) not in sys.path:
    sys.path.insert(0, str(current_file.parent))

print(f"📍 Entry point: {current_file}")
print(f"📍 Project directory: {project_dir}")
print(f"📍 Added to sys.path: {current_file.parent}")

# Import the main app logic
from new_data_assistant_project.frontend.app import main

if __name__ == "__main__":
    main()
