#!/usr/bin/env python3
"""
Data Assistant Project - Google Cloud Entry Point
This is the main entry point that Google Cloud will use.
"""

import sys
import os
from pathlib import Path
import streamlit.web.bootstrap as bootstrap
from streamlit.web.server import Server

# Setup path einmal am Anfang
current_file = Path(__file__).resolve()
project_dir = current_file / "new_data_assistant_project"

# Add the project root to sys.path for imports
if str(current_file.parent) not in sys.path:
    sys.path.insert(0, str(current_file.parent))

print(f"📍 Entry point: {current_file}")
print(f"📍 Project directory: {project_dir}")
print(f"📍 Added to sys.path: {current_file.parent}")

# Set environment variables for Google Cloud
os.environ['STREAMLIT_SERVER_PORT'] = '8080'
os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
os.environ['STREAMLIT_SERVER_ENABLE_CORS'] = 'false'
os.environ['STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION'] = 'false'

def main():
    """Main function to run the Streamlit app."""
    try:
        # Import the main app logic
        from new_data_assistant_project.frontend.app import main as app_main
        
        # Run the Streamlit app
        print("🚀 Starting Data Assistant Project on Google Cloud...")
        print(f"🌐 Server will be available at: http://0.0.0.0:8080")
        
        # Run the app
        app_main()
        
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
