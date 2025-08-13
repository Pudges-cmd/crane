#!/usr/bin/env python3
"""
Camera Detection Utility for Raspberry Pi 4B
Detects and lists available USB cameras and Pi Camera.
"""

import cv2
import os
import subprocess

def detect_cameras():
    """Detect available cameras on the system"""
    print("Camera Detection Utility")
    print("=" * 40)
    
    cameras = []
    
    # Test camera indices 0-10
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            # Get camera info
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            # Try to get a frame to verify camera works
            ret, frame = cap.read()
            if ret:
                cameras.append({
                    'index': i,
                    'width': width,
                    'height': height,
                    'fps': fps,
                    'working': True
                })
                print(f"Camera {i}: {width}x{height} @ {fps:.1f}fps - WORKING")
            else:
                print(f"Camera {i}: {width}x{height} @ {fps:.1f}fps - NO FRAME")
            
            cap.release()
        else:
            print(f"Camera {i}: Not available")
    
    # Check for Pi Camera specifically
    try:
        result = subprocess.run(['vcgencmd', 'get_camera'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"\nPi Camera Status: {result.stdout.strip()}")
    except:
        print("\nPi Camera Status: Could not check (not on Raspberry Pi)")
    
    # List USB devices
    try:
        result = subprocess.run(['lsusb'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("\nUSB Devices:")
            for line in result.stdout.strip().split('\n'):
                if 'camera' in line.lower() or 'webcam' in line.lower() or 'video' in line.lower():
                    print(f"  {line}")
    except:
        print("\nUSB Devices: Could not check")
    
    print("\n" + "=" * 40)
    if cameras:
        print(f"Found {len(cameras)} working camera(s)")
        print("Recommended settings for config.py:")
        print(f"CAMERA_INDEX = {cameras[0]['index']}  # First working camera")
        print(f"CAMERA_WIDTH = {cameras[0]['width']}")
        print(f"CAMERA_HEIGHT = {cameras[0]['height']}")
    else:
        print("No working cameras found!")
        print("Check your camera connections and permissions.")
    
    return cameras

if __name__ == "__main__":
    detect_cameras()
