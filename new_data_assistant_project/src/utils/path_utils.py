"""
Path utilities for the Data Assistant Project.
Handles absolute paths for both local and Streamlit Cloud environments.
"""

import os
from pathlib import Path

def is_streamlit_cloud():
    """Check if running in Streamlit Cloud environment."""
    return os.environ.get('STREAMLIT_SERVER_RUN_ON_FILE_CHANGE') is not None

def get_project_root():
    """Get the absolute path to the project root directory."""
    if is_streamlit_cloud():
        # In Streamlit Cloud: /mount/src/data_assistant_project
        return Path("/mount/src/data_assistant_project")
    else:
        # Local development: navigate from current file
        current_file = Path(__file__).resolve()
        # Navigate from src/utils/path_utils.py to project root
        # We're in: .../data_assistant_project/new_data_assistant_project/src/utils/path_utils.py
        # So we need to go up 4 levels to reach data_assistant_project root
        project_root = current_file.parent.parent.parent.parent
        return project_root

def get_absolute_path(relative_path):
    """
    Convert a relative path to an absolute path from the project root.
    
    Args:
        relative_path (str): Path relative to project root (e.g., 'new_data_assistant_project/src/database/superstore.db')
    
    Returns:
        Path: Absolute path to the file/directory
    """
    project_root = get_project_root()
    absolute_path = project_root / relative_path
    return absolute_path

def get_data_path():
    """Get the absolute path to the data directory."""
    return get_absolute_path('new_data_assistant_project/data')

def get_database_path():
    """Get the absolute path to the database directory."""
    return get_absolute_path('new_data_assistant_project/src/database')

def get_frontend_path():
    """Get the absolute path to the frontend directory."""
    return get_absolute_path('new_data_assistant_project/frontend')

def ensure_directory_exists(path):
    """Ensure a directory exists, create it if it doesn't."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def debug_paths():
    """Debug function to print all important paths."""
    print("🔍 Path Debug Information:")
    print(f"  Project Root: {get_project_root()}")
    print(f"  Data Path: {get_data_path()}")
    print(f"  Database Path: {get_database_path()}")
    print(f"  Frontend Path: {get_frontend_path()}")
    print(f"  Current Working Directory: {os.getcwd()}")
    print(f"  Is Streamlit Cloud: {is_streamlit_cloud()}")
    print(f"  __file__: {__file__}") 