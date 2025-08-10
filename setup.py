#!/usr/bin/env python3
"""
Setup script for LightShot Security Research Tool

This script helps set up the environment and dependencies for the research tool.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True


def install_requirements():
    """Install required packages from requirements.txt."""
    try:
        print("📦 Installing requirements...")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False


def check_chrome():
    """Check if Chrome browser is available."""
    try:
        if platform.system() == "Windows":
            # Check common Chrome installation paths on Windows
            chrome_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            ]
            for path in chrome_paths:
                if os.path.exists(path):
                    print("✅ Google Chrome found")
                    return True
        else:
            # Try to run chrome command on Unix-like systems
            subprocess.check_output(
                ["which", "google-chrome"], stderr=subprocess.DEVNULL
            )
            print("✅ Google Chrome found")
            return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    print("⚠️  Google Chrome not found. Please install Chrome browser.")
    return False


def check_chromedriver():
    """Check if ChromeDriver is available."""
    driver_paths = [
        "driver/chromedriver_win32/chromedriver.exe",
        "driver/chromedriver_win32 (1)/chromedriver.exe",
    ]

    for path in driver_paths:
        if os.path.exists(path):
            print(f"✅ ChromeDriver found at: {path}")
            return True

    print("⚠️  ChromeDriver not found in expected locations.")
    print("   Please ensure ChromeDriver is in the driver/ directory.")
    return False


def create_directories():
    """Create necessary directories."""
    directories = ["images", "logs"]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Directory created/verified: {directory}")


def display_usage_info():
    """Display basic usage information."""
    print("\n" + "=" * 60)
    print("🚀 Setup Complete!")
    print("=" * 60)
    print("\n📖 Basic Usage:")
    print("   python main.py")
    print("\n🔧 Advanced Options:")
    print("   python main.py --help")
    print("\n⚠️  Remember:")
    print("   - This tool is for educational purposes only")
    print("   - Use appropriate delays between requests")
    print("   - Respect terms of service and rate limits")
    print("\n📝 Logs will be saved to: lightshot_research.log")
    print("🖼️  Screenshots will be saved to: images/")


def main():
    """Main setup function."""
    print("🔧 LightShot Security Research Tool - Setup")
    print("=" * 50)

    success = True

    # Check Python version
    if not check_python_version():
        success = False

    # Install requirements
    if success and not install_requirements():
        success = False

    # Check Chrome
    if not check_chrome():
        success = False

    # Check ChromeDriver
    if not check_chromedriver():
        success = False

    # Create directories
    create_directories()

    if success:
        display_usage_info()
        return 0
    else:
        print("\n❌ Setup completed with warnings.")
        print("   Please address the issues above before running the tool.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
