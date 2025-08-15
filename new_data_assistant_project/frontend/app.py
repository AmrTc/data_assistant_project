import os
import sys
from pathlib import Path
import streamlit as st
import logging

# AUTO-NAVIGATE TO CORRECT DIRECTORY & SETUP IMPORTS
def ensure_correct_working_directory():
    """Simple setup for Streamlit - use normal imports without path manipulation."""
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent
    
    print(f"📍 App location: {current_file}")
    print(f"📍 Project root: {project_root}")
    print(f"📍 Working directory: {os.getcwd()}")
    
    # Don't change directories or manipulate sys.path
    # Let Streamlit handle the imports naturally
    print("✅ Using normal Streamlit imports - no path manipulation needed")

# Execute directory navigation before any other imports
ensure_correct_working_directory()

# Helper function for environment-aware page imports
def import_page_module(module_name, function_name):
    """Import page modules using environment-aware imports."""
    import os
    is_streamlit_cloud = os.environ.get('STREAMLIT_SERVER_RUN_ON_FILE_CHANGE') is not None
    
    if is_streamlit_cloud:
        # In Streamlit Cloud, use the full project path
        try:
            module = __import__(f"new_data_assistant_project.frontend.pages.{module_name}", fromlist=[function_name])
            return getattr(module, function_name)
        except ImportError as e:
            print(f"❌ Streamlit Cloud import failed for {module_name}: {e}")
            return None
    else:
        # In local environment, try multiple import strategies
        try:
            # Try direct import
            module = __import__(f"frontend.pages.{module_name}", fromlist=[function_name])
            return getattr(module, function_name)
        except ImportError:
            try:
                # Try full project path
                module = __import__(f"new_data_assistant_project.frontend.pages.{module_name}", fromlist=[function_name])
                return getattr(module, function_name)
            except ImportError:
                try:
                    # Try relative import
                    module = __import__(f"pages.{module_name}", fromlist=[function_name])
                    return getattr(module, function_name)
                except ImportError as e:
                    print(f"❌ Local import failed for {module_name}: {e}")
                    return None

# Simple import function for Streamlit
def simple_import():
    """Import required modules using environment-aware imports for Streamlit Cloud."""
    
    # Check if we're running in Streamlit Cloud or local environment
    import os
    is_streamlit_cloud = os.environ.get('STREAMLIT_SERVER_RUN_ON_FILE_CHANGE') is not None
    
    if is_streamlit_cloud:
        print("🌐 Detected Streamlit Cloud environment")
        # In Streamlit Cloud, use the full project path
        try:
            from new_data_assistant_project.src.utils.auth_manager import AuthManager
            from new_data_assistant_project.src.utils.chat_manager import ChatManager
            from new_data_assistant_project.src.database.schema import create_tables, create_admin_user
            print("✅ Streamlit Cloud imports successful")
            return AuthManager, ChatManager, create_tables, create_admin_user
        except ImportError as e:
            print(f"❌ Streamlit Cloud imports failed: {e}")
            st.error(f"❌ Could not import required modules in Streamlit Cloud: {e}")
            st.stop()
    else:
        print("💻 Detected local environment")
        # In local environment, try multiple import strategies
        try:
            # Try direct imports from src
            from src.utils.auth_manager import AuthManager
            from src.utils.chat_manager import ChatManager
            from src.database.schema import create_tables, create_admin_user
            print("✅ Local direct imports successful")
            return AuthManager, ChatManager, create_tables, create_admin_user
        except ImportError as e:
            print(f"❌ Local direct imports failed: {e}")
            
            try:
                # Fallback to full project path
                from new_data_assistant_project.src.utils.auth_manager import AuthManager
                from new_data_assistant_project.src.utils.chat_manager import ChatManager
                from new_data_assistant_project.src.database.schema import create_tables, create_admin_user
                print("✅ Local full path imports successful")
                return AuthManager, ChatManager, create_tables, create_admin_user
            except ImportError as e2:
                print(f"❌ Local full path imports failed: {e2}")
                st.error(f"❌ Could not import required modules locally: {e2}")
                st.error("Please ensure the project structure is correct and all dependencies are installed.")
                st.stop()

# Import modules
AuthManager, ChatManager, create_tables, create_admin_user = simple_import()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import traceback

def initialize_system():
    """Initialize system by checking directories and creating tables."""
    try:
        # Check required directories
        required_dirs = ['src', 'src/database', 'frontend']
        missing_dirs = []
        for dir_name in required_dirs:
            if not os.path.exists(dir_name):
                missing_dirs.append(dir_name)
                logger.error(f"❌ Missing directory: {dir_name}")
        
        if missing_dirs:
            logger.error(f"❌ Missing directories: {missing_dirs}")
            logger.error(f"Current directory contents: {os.listdir('.')}")
            return False
        
        # Check database file
        db_path = "src/database/superstore.db"
        if os.path.exists(db_path):
            logger.info(f"✅ Database file exists: {db_path}")
        else:
            logger.warning(f"⚠️ Database file will be created: {db_path}")
            
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
        try:
            from data_assistant_project.new_data_assistant_project.frontend.pages.welcome_page import render_welcome_page
        except ImportError:
            try:
                from new_data_assistant_project.frontend.pages.welcome_page import render_welcome_page
            except ImportError:
                try:
                    from frontend.pages.welcome_page import render_welcome_page
                except ImportError:
                    try:
                        from pages.welcome_page import render_welcome_page
                    except ImportError:
                        st.error("❌ Could not import welcome page")
                        return
        
        user = auth_manager.get_current_user()
        render_welcome_page(user)
    
    elif st.session_state.current_page == "assessment":
        try:
            from data_assistant_project.new_data_assistant_project.frontend.pages.assessment_page import render_assessment_page
        except ImportError:
            try:
                from new_data_assistant_project.frontend.pages.assessment_page import render_assessment_page
            except ImportError:
                try:
                    from frontend.pages.assessment_page import render_assessment_page
                except ImportError:
                    try:
                        from pages.assessment_page import render_assessment_page
                    except ImportError:
                        st.error("❌ Could not import assessment page")
                        return
        
        user = auth_manager.get_current_user()
        render_assessment_page(user)
    
    elif st.session_state.current_page == "task":
        try:
            from data_assistant_project.new_data_assistant_project.frontend.pages.task_page import render_task_page
        except ImportError:
            try:
                from new_data_assistant_project.frontend.pages.task_page import render_task_page
            except ImportError:
                try:
                    from frontend.pages.task_page import render_task_page
                except ImportError:
                    try:
                        from pages.task_page import render_task_page
                    except ImportError:
                        st.error("❌ Could not import task page")
                        return
        
        user = auth_manager.get_current_user()
        render_task_page(user)
    
    elif st.session_state.current_page == "data_assistant":
        user = auth_manager.get_current_user()
        chat_manager.render_chat_interface(user)
    
    elif st.session_state.current_page == "evaluation":
        # Import evaluation dashboard with same robust strategy
        try:
            from data_assistant_project.new_data_assistant_project.frontend.pages.evaluation_dashboard import render_evaluation_dashboard
        except ImportError:
            try:
                from new_data_assistant_project.frontend.pages.evaluation_dashboard import render_evaluation_dashboard
            except ImportError:
                try:
                    from frontend.pages.evaluation_dashboard import render_evaluation_dashboard
                except ImportError:
                    try:
                        from pages.evaluation_dashboard import render_evaluation_dashboard
                    except ImportError:
                        st.error("❌ Could not import evaluation dashboard")
                        return
        
        render_evaluation_dashboard()

def render_user_interface(user):
    """Render user interface with 4-page structure."""
    
    # Initialize current page if not set - default to welcome
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "welcome"
    
    # Clean sidebar separator
    st.sidebar.markdown("<div style='margin: 1rem 0; border-top: 1px solid #f0f0f0;'></div>", unsafe_allow_html=True)
    
    # Add navigation controls for users
    st.sidebar.markdown("## 🧭 Navigation")
    
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
        try:
            from data_assistant_project.new_data_assistant_project.frontend.pages.welcome_page import render_welcome_page
        except ImportError:
            try:
                from new_data_assistant_project.frontend.pages.welcome_page import render_welcome_page
            except ImportError:
                try:
                    from frontend.pages.welcome_page import render_welcome_page
                except ImportError:
                    try:
                        from pages.welcome_page import render_welcome_page
                    except ImportError:
                        st.error("❌ Could not import welcome page")
                        return
        
        render_welcome_page(user)
    
    elif st.session_state.current_page == "assessment":
        try:
            from data_assistant_project.new_data_assistant_project.frontend.pages.assessment_page import render_assessment_page
        except ImportError:
            try:
                from new_data_assistant_project.frontend.pages.assessment_page import render_assessment_page
            except ImportError:
                try:
                    from frontend.pages.assessment_page import render_assessment_page
                except ImportError:
                    try:
                        from pages.assessment_page import render_assessment_page
                    except ImportError:
                        st.error("❌ Could not import assessment page")
                        return
        
        render_assessment_page(user)
    
    elif st.session_state.current_page == "task":
        try:
            from data_assistant_project.new_data_assistant_project.frontend.pages.task_page import render_task_page
        except ImportError:
            try:
                from new_data_assistant_project.frontend.pages.task_page import render_task_page
            except ImportError:
                try:
                    from frontend.pages.task_page import render_task_page
                except ImportError:
                    try:
                        from pages.task_page import render_task_page
                    except ImportError:
                        st.error("❌ Could not import task page")
                        return
        
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
        
        try:
            from data_assistant_project.new_data_assistant_project.frontend.pages.feedback_page import render_feedback_page
        except ImportError:
            try:
                from new_data_assistant_project.frontend.pages.feedback_page import render_feedback_page
            except ImportError:
                try:
                    from frontend.pages.feedback_page import render_feedback_page
                except ImportError:
                    try:
                        from pages.feedback_page import render_feedback_page
                    except ImportError:
                        st.error("❌ Could not import feedback page")
                        return
        
        render_feedback_page(user)


if __name__ == "__main__":
    main()