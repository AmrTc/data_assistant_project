#!/usr/bin/env python3
"""
Test file to verify all imports are working correctly.
Run this from the repository root to test the new import structure.
"""

import sys
from pathlib import Path

print("🧪 Testing imports for Data Assistant Project")
print("=" * 50)

# Setup path like the main app
current_file = Path(__file__).resolve()
project_dir = current_file.parent / "new_data_assistant_project"
if str(project_dir.parent) not in sys.path:
    sys.path.insert(0, str(project_dir.parent))

print(f"📍 Test file: {current_file}")
print(f"📍 Project directory: {project_dir}")
print(f"📍 Added to sys.path: {project_dir.parent}")

# Test all major imports
try:
    print("\n🔍 Testing core imports...")
    
    # Test path_utils
    from new_data_assistant_project.src.utils.path_utils import get_project_root, get_absolute_path
    print("✅ path_utils imported successfully")
    
    # Test auth_manager
    from new_data_assistant_project.src.utils.auth_manager import AuthManager
    print("✅ auth_manager imported successfully")
    
    # Test chat_manager
    from new_data_assistant_project.src.utils.chat_manager import ChatManager
    print("✅ chat_manager imported successfully")
    
    # Test database models
    from new_data_assistant_project.src.database.models import User
    print("✅ database models imported successfully")
    
    # Test database schema
    from new_data_assistant_project.src.database.schema import create_tables, create_admin_user
    print("✅ database schema imported successfully")
    
    # Test agents
    from new_data_assistant_project.src.agents.clt_cft_agent import CLTCFTAgent
    print("✅ clt_cft_agent imported successfully")
    
    from new_data_assistant_project.src.agents.ReAct_agent import ReActAgent
    print("✅ ReAct_agent imported successfully")
    
    # Test configuration
    from new_data_assistant_project.src.utils.my_config import MyConfig
    print("✅ my_config imported successfully")
    
    # Test path utilities
    from new_data_assistant_project.src.utils.secrets_path_utils import SecretsPathUtils
    print("✅ secrets_path_utils imported successfully")
    
    print("\n🎉 All imports successful! The project is ready for Streamlit Cloud.")
    
except ImportError as e:
    print(f"\n❌ Import failed: {e}")
    print("\n🔧 Troubleshooting:")
    print("1. Make sure you're running this from the repository root")
    print("2. Check that all files have been updated with consistent imports")
    print("3. Verify the project structure is correct")
    
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Import test completed!")
