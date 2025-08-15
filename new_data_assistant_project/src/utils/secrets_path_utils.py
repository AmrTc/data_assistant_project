"""
Secrets path utilities for the Data Assistant project.
"""

import os
from pathlib import Path
import sys

# Robust import handling for different environments
def robust_import_modules():
    """Import required modules with multiple fallback strategies."""
    
    # Strategy 1: Try absolute imports (local development)
    try:
        from new_data_assistant_project.src.utils.path_utils import get_project_root, get_absolute_path
        print("✅ Secrets Path Utils: Absolute imports successful")
        return get_project_root, get_absolute_path
    except ImportError as e:
        print(f"❌ Absolute imports failed: {e}")
    
    # Strategy 2: Try direct imports (Docker/production - new structure)
    try:
        from src.utils.path_utils import get_project_root, get_absolute_path
        print("✅ Secrets Path Utils: Direct imports successful")
        return get_project_root, get_absolute_path
    except ImportError as e:
        print(f"❌ Direct imports failed: {e}")
    
    # Strategy 3: Try relative imports (fallback)
    try:
        from .path_utils import get_project_root, get_absolute_path
        print("✅ Secrets Path Utils: Relative imports successful")
        return get_project_root, get_absolute_path
    except ImportError as e:
        print(f"❌ Relative imports failed: {e}")
    
    # Strategy 4: Manual path manipulation
    try:
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        
        from new_data_assistant_project.src.utils.path_utils import get_project_root, get_absolute_path
        print("✅ Secrets Path Utils: Manual path imports successful")
        return get_project_root, get_absolute_path
    except ImportError as e:
        print(f"❌ Manual path imports failed: {e}")
        print(f"❌ Could not import required modules: {e}")
        return None, None

# Import modules
get_project_root, get_absolute_path = robust_import_modules()

class SecretsPathUtils:
    """Utility class for managing paths to secret files and configurations."""
    
    _instance = None
    
    def __init__(self):
        """Initialize SecretsPathUtils with project root detection."""
        # Use more robust project root detection
        current_file = Path(__file__).resolve()
        
        # Find the data_assistant_project directory that contains src/
        project_root = current_file
        while project_root.name != 'data_assistant_project' and project_root.parent != project_root:
            project_root = project_root.parent
        
        # If we found a data_assistant_project but it doesn't have src/, look for nested one
        if project_root.name == 'data_assistant_project':
            if not (project_root / 'src').exists():
                # Look for nested data_assistant_project
                nested_project = project_root / 'data_assistant_project'
                if nested_project.exists() and (nested_project / 'src').exists():
                    project_root = nested_project
        
        self.project_root = project_root
        
        # Define secrets directory - always in the outer project root
        if (project_root / 'src').exists():
            # We're in the inner project, go to outer for secrets
            secrets_root = project_root.parent
        else:
            # We're in the outer project
            secrets_root = project_root
        
        self.secrets_dir = secrets_root / 'secrets'
        
        # Ensure secrets directory exists
        self.secrets_dir.mkdir(exist_ok=True)
    
    def get_env_file_path(self) -> Path:
        """Get path to .env file in secrets directory."""
        return self.secrets_dir / '.env'
    
    def get_secrets_dir(self) -> Path:
        """Get path to secrets directory."""
        return self.secrets_dir
    
    @classmethod
    def get_instance(cls):
        """Get or create singleton instance of SecretsPathUtils."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

if __name__ == "__main__":
    # Test the utility
    try:
        secrets_utils = SecretsPathUtils.get_instance()
        
        print("\nSecrets Directory Test:")
        secrets_dir = secrets_utils.get_secrets_dir()
        print(f"Secrets directory: {secrets_dir}")
        print(f"Directory exists: {'Yes' if secrets_dir.exists() else 'No'}")
        
        print("\nEnvironment File Test:")
        env_path = secrets_utils.get_env_file_path()
        print(f".env file location: {env_path}")
        print(f".env file exists: {'Yes' if env_path.exists() else 'No'}")
        
    except Exception as e:
        print(f"\nError occurred: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you're running this from within the project directory")
        print("2. Check if the project structure is correct")
        print("3. Ensure you have write permissions in the secrets directory") 