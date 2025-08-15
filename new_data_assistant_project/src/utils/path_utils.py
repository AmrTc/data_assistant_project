"""
Path utilities for the Data Assistant Project.
Handles absolute paths for both local and Streamlit Cloud environments.
"""

import os
import sys
from pathlib import Path

# Path Setup am Anfang jeder Datei - gleiche Strategie wie in app.py
current_file = Path(__file__).resolve()
project_dir = current_file.parent.parent.parent.parent
if str(project_dir.parent) not in sys.path:
    sys.path.insert(0, str(project_dir.parent))

def get_project_root():
<<<<<<< HEAD
    """Get the absolute path to the project root directory."""
    return project_dir.parent
=======
    """Get the absolute path to the new_data_assistant_project directory."""
    current_file = Path(__file__).resolve()
    # Navigate from src/utils/path_utils.py to new_data_assistant_project root
    # We're in: .../new_data_assistant_project/src/utils/path_utils.py
    # So we need to go up 3 levels to reach new_data_assistant_project
    project_root = current_file.parent.parent.parent
    return project_root
>>>>>>> 88e9b37 (ahhhhhhhhh)

def get_absolute_path(relative_path):
    """
    Convert a relative path to an absolute path from the new_data_assistant_project root.
    
    Args:
<<<<<<< HEAD
        relative_path (str): Path relative to project root (e.g., 'new_data_assistant_project/src/database/superstore.db')
=======
        relative_path (str): Path relative to new_data_assistant_project root (e.g., 'src/database/superstore.db')
>>>>>>> 88e9b37 (ahhhhhhhhh)
    
    Returns:
        Path: Absolute path to the file/directory
    """
    project_root = get_project_root()
    absolute_path = project_root / relative_path
    return absolute_path

def get_data_path():
    """Get the absolute path to the data directory."""
    return get_absolute_path('data')

def get_database_path():
    """Get the absolute path to the database directory."""
    return get_absolute_path('src/database')

def get_frontend_path():
    """Get the absolute path to the frontend directory."""
    return get_absolute_path('frontend')

def ensure_directory_exists(path):
    """Ensure a directory exists, create it if it doesn't."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def is_streamlit_cloud():
    """Check if running in Streamlit Cloud environment."""
    return os.environ.get('STREAMLIT_SERVER_RUN_ON_FILE_CHANGE') is not None

def debug_paths():
    """Debug function to print all important paths."""
    print("🔍 Path Debug Information:")
    print(f"  Project Root (new_data_assistant_project): {get_project_root()}")
    print(f"  Data Path: {get_data_path()}")
    print(f"  Database Path: {get_database_path()}")
    print(f"  Frontend Path: {get_frontend_path()}")
    print(f"  Current Working Directory: {os.getcwd()}")
    print(f"  Is Streamlit Cloud: {is_streamlit_cloud()}")
    print(f"  __file__: {__file__}") 