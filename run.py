#!/usr/bin/env python3
"""
Go-Bike-Network-Analysis - Runner Script
Simple and efficient application launcher
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    return True

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import streamlit
        import pandas
        import plotly
        import folium
        import scipy
        import matplotlib
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

def check_data_file():
    """Check if data file exists"""
    data_file = "201902-fordgobike-tripdata.csv"
    if not os.path.exists(data_file):
        print(f"❌ Data file not found: {data_file}")
        print("📥 Download from: https://s3.amazonaws.com/baywheels-data/index.html")
        return False
    return True

def main():
    """Main runner function"""
    print("🚲 Go-Bike-Network-Analysis")
    print("=" * 40)
    
    # Environment checks
    if not check_python_version():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    if not check_data_file():
        print("\n⚠️  You can still run the app, but some features may not work.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    print("✅ All checks passed!")
    print("🚀 Starting Streamlit application...")
    print("📱 Open your browser to the URL shown below")
    print("=" * 40)
    
    # Launch Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app/main.py", "--server.port", "8501"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 