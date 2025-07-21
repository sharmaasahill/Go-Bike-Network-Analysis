#!/usr/bin/env python3
"""
Simple runner script for Modern Bike Analytics Platform
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 9):
        print("Error: Python 3.9 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_data_file():
    """Check if the data file exists"""
    data_file = "201902-fordgobike-tripdata.csv"
    if not os.path.exists(data_file):
        print(f"Error: Data file '{data_file}' not found")
        print("Please ensure the Ford GoBike dataset is in the project root directory")
        return False
    return True

def install_dependencies():
    """Install required dependencies"""
    try:
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False

def run_application():
    """Run the Streamlit application"""
    try:
        print("Starting Modern Bike Analytics Platform...")
        print("Dashboard will be available at: http://localhost:8501")
        print("Press Ctrl+C to stop the application")
        print("-" * 50)
        
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app/main.py", 
            "--server.port=8501",
            "--server.headless=true"
        ])
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error running application: {e}")

def main():
    """Main function"""
    print("Modern Bike Analytics Platform")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check data file
    if not check_data_file():
        sys.exit(1)
    
    # Install dependencies if needed
    try:
        import streamlit
        import plotly
        import pandas
        print("All dependencies are already installed")
    except ImportError:
        if not install_dependencies():
            sys.exit(1)
    
    # Run the application
    run_application()

if __name__ == "__main__":
    main() 