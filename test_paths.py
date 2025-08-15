#!/usr/bin/env python3
"""
Test file to verify path utilities are working correctly.
Run this from the repository root to test the path resolution.
"""

import sys
from pathlib import Path

print("🧪 Testing path utilities for Data Assistant Project")
print("=" * 50)

# Setup path like the main app
current_file = Path(__file__).resolve()
project_dir = current_file.parent / "new_data_assistant_project"
if str(project_dir.parent) not in sys.path:
    sys.path.insert(0, str(project_dir.parent))

print(f"📍 Test file: {current_file}")
print(f"📍 Project directory: {project_dir}")
print(f"📍 Added to sys.path: {project_dir.parent}")

# Test path utilities
try:
    print("\n🔍 Testing path utilities...")
    
    from new_data_assistant_project.src.utils.path_utils import (
        get_project_root, 
        get_absolute_path, 
        get_database_path, 
        get_frontend_path,
        debug_paths
    )
    
    print("✅ path_utils imported successfully")
    
    # Test path resolution
    print("\n📍 Testing path resolution:")
    
    project_root = get_project_root()
    print(f"  Project Root: {project_root}")
    print(f"  Project Root exists: {project_root.exists()}")
    
    db_path = get_database_path()
    print(f"  Database Path: {db_path}")
    print(f"  Database Path exists: {db_path.exists()}")
    
    frontend_path = get_frontend_path()
    print(f"  Frontend Path: {frontend_path}")
    print(f"  Frontend Path exists: {frontend_path.exists()}")
    
    # Test specific paths
    db_file = get_absolute_path('new_data_assistant_project/src/database/superstore.db')
    print(f"  Database File: {db_file}")
    print(f"  Database File exists: {db_file.exists()}")
    
    # Test directory structure
    print("\n📂 Testing directory structure:")
    required_dirs = ['src', 'src/database', 'frontend']
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        print(f"  {dir_name}: {dir_path} - {'✅ Exists' if dir_path.exists() else '❌ Missing'}")
    
    print("\n🎉 Path utilities test completed successfully!")
    
except ImportError as e:
    print(f"\n❌ Import failed: {e}")
    
except Exception as e:
    print(f"\n❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Path test completed!")
