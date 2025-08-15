#!/usr/bin/env python3
"""
Script to create test users for the Intelligent Explanation System.
"""

import logging
import random
from typing import Dict, Any, List
import uuid
from datetime import datetime
import sys
from pathlib import Path

# Robust import handling for different environments
def robust_import_modules():
    """Import required modules with multiple fallback strategies."""
    
    # Strategy 1: Try absolute imports (local development)
    try:
        from new_data_assistant_project.src.database.models import User
        from new_data_assistant_project.src.utils.path_utils import get_absolute_path
        print("✅ Create Test Users: Absolute imports successful")
        return User, get_absolute_path
    except ImportError as e:
        print(f"❌ Absolute imports failed: {e}")
    
    # Strategy 2: Try direct imports (Docker/production - new structure)
    try:
        from src.database.models import User
        from src.utils.path_utils import get_absolute_path
        print("✅ Create Test Users: Direct imports successful")
        return User, get_absolute_path
    except ImportError as e:
        print(f"❌ Direct imports failed: {e}")
    
    # Strategy 3: Try relative imports (fallback)
    try:
        from ..database.models import User
        from .path_utils import get_absolute_path
        print("✅ Create Test Users: Relative imports successful")
        return User, get_absolute_path
    except ImportError as e:
        print(f"❌ Relative imports failed: {e}")
    
    # Strategy 4: Manual path manipulation
    try:
        current_file = Path(__file__).resolve()
        project_root = current_file.parent.parent.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))
        
        from new_data_assistant_project.src.database.models import User
        from new_data_assistant_project.src.utils.path_utils import get_absolute_path
        print("✅ Create Test Users: Manual path imports successful")
        return User, get_absolute_path
    except ImportError as e:
        print(f"❌ Manual path imports failed: {e}")
        print(f"❌ Could not import required modules: {e}")
        return None, None

# Import modules
User, get_absolute_path = robust_import_modules()

if User is None or get_absolute_path is None:
    print("❌ Failed to import required modules. Exiting.")
    exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_users():
    """Create test users with different expertise levels."""
    db_path = get_absolute_path('new_data_assistant_project/src/database/superstore.db')
    
    test_users = [
        {
            'username': 'test_user',
            'email': 'test@example.com',
            'password': 'test123',
            'name': 'Test User',
            'sql_level': 2,
            'domain_level': 2
        },
        {
            'username': 'beginner_user',
            'email': 'beginner@example.com',
            'password': 'test123',
            'name': 'Beginner User',
            'sql_level': 1,
            'domain_level': 1
        },
        {
            'username': 'intermediate_user',
            'email': 'intermediate@example.com',
            'password': 'test123',
            'name': 'Intermediate User',
            'sql_level': 3,
            'domain_level': 3
        },
        {
            'username': 'expert_user',
            'email': 'expert@example.com',
            'password': 'test123',
            'name': 'Expert User',
            'sql_level': 5,
            'domain_level': 5
        }
    ]
    
    for user_data in test_users:
        try:
            # Check if user already exists
            existing_user = User.get_by_username(db_path, user_data['username'])
            if existing_user:
                logger.info(f"User {user_data['username']} already exists")
                continue
            
            # Create new user
            user = User.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                name=user_data['name']
            )
            
            # Complete assessment automatically for test users
            user.complete_assessment(
                db_path, 
                user_data['sql_level'], 
                user_data['domain_level']
            )
            
            logger.info(f"Created test user: {user_data['username']} (SQL: {user_data['sql_level']}, Domain: {user_data['domain_level']})")
            
        except Exception as e:
            logger.error(f"Error creating user {user_data['username']}: {e}")
    
    logger.info("Test user creation completed!")
    print("\n" + "="*60)
    print("TEST USERS CREATED SUCCESSFULLY!")
    print("="*60)
    print("Available test accounts:")
    print("  📚 beginner_user / test123    (SQL: 1/5, Domain: 1/5)")
    print("  📊 intermediate_user / test123 (SQL: 3/5, Domain: 3/5)")
    print("  🎓 expert_user / test123      (SQL: 5/5, Domain: 5/5)")
    print("  🧪 test_user / test123        (SQL: 2/5, Domain: 2/5)")
    print("\nAdmin account:")
    print("  🔧 admin / admin123           (Full system access)")
    print("="*60)

if __name__ == "__main__":
    create_test_users() 