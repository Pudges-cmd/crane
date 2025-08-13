#!/usr/bin/env python3
"""
Setup script for Raspberry Pi Motor Control with YOLOv5
Handles installation and configuration for the project.
"""

import os
import sys
import subprocess
import platform
import shutil

def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_system():
    """Check if running on Raspberry Pi"""
    print("🔍 Checking system requirements...")
    
    # Check if running on Raspberry Pi
    if not os.path.exists('/proc/device-tree/model'):
        print("⚠️  Warning: This script is designed for Raspberry Pi")
        print("   It may work on other systems but is not guaranteed")
    else:
        with open('/proc/device-tree/model', 'r') as f:
            model = f.read().strip()
            print(f"✅ Detected: {model}")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 9):
        print(f"❌ Python 3.9+ required, found {python_version.major}.{python_version.minor}")
        return False
    else:
        print(f"✅ Python {python_version.major}.{python_version.minor} detected")
    
    return True

def update_system():
    """Update system packages"""
    print("\n📦 Updating system packages...")
    
    commands = [
        ("sudo apt update", "Updating package list"),
        ("sudo apt upgrade -y", "Upgrading packages"),
        ("sudo apt install -y python3-pip python3-opencv libatlas-base-dev git build-essential cmake pkg-config", "Installing dependencies")
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def install_python_packages():
    """Install Python packages"""
    print("\n🐍 Installing Python packages...")
    
    # Upgrade pip first
    if not run_command("pip3 install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install packages from requirements.txt
    if os.path.exists('requirements.txt'):
        if not run_command("pip3 install -r requirements.txt", "Installing Python packages"):
            return False
    else:
        print("❌ requirements.txt not found")
        return False
    
    return True

def check_camera():
    """Check camera availability"""
    print("\n📷 Checking camera...")
    
    # Check for Pi Camera
    if os.path.exists('/dev/video0'):
        print("✅ Camera device found at /dev/video0")
    else:
        print("⚠️  No camera device found at /dev/video0")
        print("   Make sure your camera is connected")
    
    # Check camera modules
    try:
        result = subprocess.run("lsmod | grep camera", shell=True, capture_output=True, text=True)
        if result.stdout:
            print("✅ Camera modules loaded")
        else:
            print("⚠️  No camera modules detected")
    except:
        pass
    
    return True

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ['logs', 'models', 'data']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")
    
    return True

def test_imports():
    """Test if all required packages can be imported"""
    print("\n🧪 Testing imports...")
    
    required_packages = [
        'cv2',
        'numpy',
        'torch',
        'torchvision',
        'ultralytics',
        'RPi.GPIO'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n⚠️  Failed to import: {', '.join(failed_imports)}")
        print("   Try running: pip3 install -r requirements.txt")
        return False
    
    return True

def main():
    """Main setup function"""
    print("🚀 Raspberry Pi Motor Control Setup")
    print("=" * 50)
    
    # Check system requirements
    if not check_system():
        print("❌ System requirements not met")
        sys.exit(1)
    
    # Update system
    if not update_system():
        print("❌ System update failed")
        sys.exit(1)
    
    # Install Python packages
    if not install_python_packages():
        print("❌ Python package installation failed")
        sys.exit(1)
    
    # Check camera
    check_camera()
    
    # Create directories
    if not create_directories():
        print("❌ Directory creation failed")
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("❌ Import test failed")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Connect your motor and camera hardware")
    print("2. Edit config.py to match your setup")
    print("3. Test motor: python3 test_motor.py")
    print("4. Test camera: python3 test_camera.py")
    print("5. Run main program: python3 motor_control_config.py")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()
