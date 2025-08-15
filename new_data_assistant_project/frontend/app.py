import os
import sys
from pathlib import Path
import streamlit as st
import logging

# Path Setup am Anfang jeder Datei
current_file = Path(__file__).resolve()
project_dir = current_file.parent.parent.parent
if str(project_dir.parent) not in sys.path:
    sys.path.insert(0, str(project_dir.parent))

print(f"📍 App location: {current_file}")
print(f"📍 Project directory: {project_dir}")
print(f"📍 Working directory: {os.getcwd()}")
print(f"📍 sys.path (first 3): {sys.path[:3]}")

# Konsistente Imports - Immer vollständige Pfade
from new_data_assistant_project.src.utils.auth_manager import AuthManager
from new_data_assistant_project.src.utils.chat_manager import ChatManager
from new_data_assistant_project.src.database.schema import create_tables, create_admin_user

print("✅ All imports successful")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import traceback

def initialize_system():
    """Initialize system by checking directories and creating tables."""
    try:
        # Import path utilities
        from new_data_assistant_project.src.utils.path_utils import debug_paths, get_database_path, ensure_directory_exists
        
        # Debug paths
        debug_paths()
        
        # Check required directories
        required_dirs = ['new_data_assistant_project/src', 'new_data_assistant_project/src/database', 'new_data_assistant_project/frontend']
        missing_dirs = []
        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            if not dir_path.exists():
                missing_dirs.append(dir_name)
                logger.error(f"❌ Missing directory: {dir_name}")
        
        if missing_dirs:
            logger.error(f"❌ Missing directories: {missing_dirs}")
            logger.error(f"Current directory contents: {os.listdir('.')}")
            return False
        
        # Check database file
        db_path = get_database_path() / "superstore.db"
        if db_path.exists():
            logger.info(f"✅ Database file exists: {db_path}")
        else:
            logger.warning(f"⚠️ Database file will be created: {db_path}")
            # Ensure database directory exists
            ensure_directory_exists(db_path.parent)
            
        # Initialize database
        create_tables()
        create_admin_user()
        
        logger.info("🎯 System initialized successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ System initialization error: {e}")
        logger.error(f"📍 Current working directory: {os.getcwd()}")
        logger.error(f"📂 Directory contents: {os.listdir('.')}")
        logger.error(f"🔍 Full traceback: {traceback.format_exc()}")
        return False

# Initialize system
system_ready = initialize_system()

if not system_ready:
    st.error("❌ System initialization failed. Please check the logs.")
    st.stop()

# Initialize managers
auth_manager = AuthManager()
chat_manager = ChatManager()

def main():
    """Main application logic with authentication and role-based routing."""
    
    # Initialize session state for current page
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "welcome"
    
    # Check authentication
    if not auth_manager.is_authenticated():
        auth_manager.render_login_page()
        return
    
    # Get current user
    user = auth_manager.get_current_user()
    
    # Render user info in sidebar
    auth_manager.render_user_info()
    
    # Users go directly to welcome page after registration
    # Assessment is optional and can be accessed via navigation
    
    # Role-based navigation and content
    if user.role == 'admin':
        render_admin_interface()
    else:
        render_user_interface(user)

def render_admin_interface():
    """Render admin interface with navigation."""
    
    # Add navigation controls for admin
    st.sidebar.markdown("## 🎯 Admin Navigation")
    
    # Navigation buttons
    if st.sidebar.button("🏠 Welcome", key="admin_welcome"):
        st.session_state.current_page = "welcome"
        st.rerun()
    
    if st.sidebar.button("📊 Assessment", key="admin_assessment"):
        st.session_state.current_page = "assessment"
        st.rerun()
    
    if st.sidebar.button("💼 Task Phase", key="admin_task"):
        st.session_state.current_page = "task"
        st.rerun()
    
    if st.sidebar.button("🤖 Data Assistant", key="admin_data_assistant"):
        st.session_state.current_page = "data_assistant"
        st.rerun()
    
    if st.sidebar.button("📈 Evaluation Dashboard", key="admin_evaluation"):
        st.session_state.current_page = "evaluation"
        st.rerun()
    
    # Direct page routing without sidebar navigation
    if st.session_state.current_page == "welcome":
        from new_data_assistant_project.frontend.pages.welcome_page import render_welcome_page
        user = auth_manager.get_current_user()
        render_welcome_page(user)
    
    elif st.session_state.current_page == "assessment":
        from new_data_assistant_project.frontend.pages.assessment_page import render_assessment_page
        user = auth_manager.get_current_user()
        render_assessment_page(user)
    
    elif st.session_state.current_page == "task":
        from new_data_assistant_project.frontend.pages.task_page import render_task_page
        user = auth_manager.get_current_user()
        render_task_page(user)
    
    elif st.session_state.current_page == "data_assistant":
        user = auth_manager.get_current_user()
        chat_manager.render_chat_interface(user)
    
    elif st.session_state.current_page == "evaluation":
        from new_data_assistant_project.frontend.pages.evaluation_dashboard import render_evaluation_dashboard
        render_evaluation_dashboard()

def render_user_interface(user):
    """Render user interface with 4-page structure."""
    
    # Initialize current page if not set - default to welcome
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "welcome"
    
    # Clean sidebar separator
    st.sidebar.markdown("<div style='margin: 1rem 0; border-top: 1px solid #f0f0f0;'></div>", unsafe_allow_html=True)
    
    # Add navigation controls for users
    st.sidebar.markdown("## �� Navigation")
    
    # Navigation buttons
    if st.sidebar.button("🏠 Welcome", key="user_welcome"):
        st.session_state.current_page = "welcome"
        st.rerun()
    
    if st.sidebar.button("📊 Assessment", key="user_assessment"):
        st.session_state.current_page = "assessment"
        st.rerun()
    
    if st.sidebar.button("💼 Task Phase", key="user_task"):
        st.session_state.current_page = "task"
        st.rerun()
    
    if st.sidebar.button("🤖 Data Assistant", key="user_data_assistant"):
        st.session_state.current_page = "data_assistant"
        st.rerun()
    
    if st.sidebar.button("📝 Feedback", key="user_feedback"):
        st.session_state.current_page = "feedback"
        st.rerun()
    
    # Page routing
    if st.session_state.current_page == "welcome":
        from new_data_assistant_project.frontend.pages.welcome_page import render_welcome_page
        render_welcome_page(user)
    
    elif st.session_state.current_page == "assessment":
        from new_data_assistant_project.frontend.pages.assessment_page import render_assessment_page
        render_assessment_page(user)
    
    elif st.session_state.current_page == "task":
        from new_data_assistant_project.frontend.pages.task_page import render_task_page
        render_task_page(user)
    
    elif st.session_state.current_page == "data_assistant":
        user = auth_manager.get_current_user()
        chat_manager.render_chat_interface(user)
    
    elif st.session_state.current_page == "feedback":
        # Check if user has completed tasks
        if not st.session_state.get('tasks_completed', False):
            st.error("❌ You must complete all tasks before accessing the feedback page.")
            st.info("Please return to the Task Phase and complete all 8 tasks.")
            st.session_state.current_page = "task"
            st.rerun()
            return
        
        from new_data_assistant_project.frontend.pages.feedback_page import render_feedback_page
        render_feedback_page(user)


if __name__ == "__main__":
    main()