#!/usr/bin/env python3
"""
Data Assistant Project - Main Entry Point
Alternative entry point for containerized environments.
"""

import sys
import os
from pathlib import Path
import subprocess

def main():
    """Main function to run the Streamlit app."""
    try:
        print("🚀 Starting Data Assistant Project...")
        print(f"🌐 Server will be available at: http://0.0.0.0:8080")
        
        # Start Streamlit using subprocess
        cmd = [
            sys.executable, "-m", "streamlit", "run",
            "frontend/app.py",
            "--server.port", "8080",
            "--server.address", "0.0.0.0",
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ]
        
        print(f"🔧 Running command: {' '.join(cmd)}")
        subprocess.run(cmd, check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Streamlit process failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting app: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
