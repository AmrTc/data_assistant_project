import os
import sys
from pathlib import Path

# Get the directory where this file is located in the project root
CURRENT_DIR = Path(__file__).parent.absolute()

# Debug output for Streamlit Cloud
print(f"📍 Streamlit entry point directory: {CURRENT_DIR}")
print(f"📍 Working directory: {os.getcwd()}")

try:
    # Simple import - let Streamlit handle the paths naturally
    from frontend.app import main
    print("✅ Successfully imported main from frontend.app")
    
except ImportError as exc:
    print(f"❌ Import error: {exc}")
    print(f"📍 Current working directory: {os.getcwd()}")
    print(f"📂 Available files in current dir: {list(CURRENT_DIR.iterdir())}")
    
    # Check if frontend directory exists
    frontend_dir = CURRENT_DIR / 'frontend'
    if frontend_dir.exists():
        print(f"📁 Frontend directory contents: {list(frontend_dir.iterdir())}")
    else:
        print("❌ Frontend directory not found")
    
    raise RuntimeError(f"Could not import main from frontend.app") from exc

if __name__ == "__main__":
    main()