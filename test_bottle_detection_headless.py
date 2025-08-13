#!/usr/bin/env python3
"""
Bottle Detection Test Script (Headless) for Raspberry Pi 4B
Tests YOLOv8 detection specifically for bottles without GUI display.
Optimized for Raspberry Pi performance and headless operation.
"""

import cv2
import time
import os
from ultralytics import YOLO
from config import *

def test_bottle_detection():
    """Test bottle detection functionality without GUI"""
    print("Bottle Detection Test Script (Headless)")
    print("This will test YOLOv8 detection specifically for bottles")
    print("Press Ctrl+C to stop")
    
    # Initialize camera with auto-detection
    camera = None
    camera_index = CAMERA_INDEX
    
    if CAMERA_AUTO_DETECT:
        print("Auto-detecting cameras...")
        # Try to find a working camera
        for i in range(5):  # Try indices 0-4
            test_camera = cv2.VideoCapture(i)
            if test_camera.isOpened():
                ret, frame = test_camera.read()
                if ret:
                    camera_index = i
                    print(f"Found working camera at index {i}")
                    test_camera.release()
                    break
                test_camera.release()
    
    camera = cv2.VideoCapture(camera_index)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    
    if not camera.isOpened():
        print(f"Error: Could not open camera at index {camera_index}")
        print("Try running 'python3 camera_detector.py' to find available cameras")
        return
    
    print(f"Camera initialized at index {camera_index}, resolution: {CAMERA_WIDTH}x{CAMERA_HEIGHT}")
    
    # Load YOLOv8 model
    try:
        if MODEL_PATH and os.path.exists(MODEL_PATH):
            model = YOLO(MODEL_PATH)
            print(f"Loaded local model: {MODEL_PATH}")
        else:
            model = YOLO('yolov8n.pt')  # Use default YOLOv8n model
            print("Using default YOLOv8n model")
    except Exception as e:
        print(f"Error loading YOLOv8 model: {e}")
        return
    
    # Get class names from the model
    class_names = model.names
    print(f"Available classes: {list(class_names.values())}")
    
    # Find bottle class ID
    bottle_class_id = None
    for class_id, class_name in class_names.items():
        if class_name.lower() == 'bottle':
            bottle_class_id = class_id
            break
    
    if bottle_class_id is None:
        print("Warning: 'bottle' class not found in model. Will detect all objects.")
        bottle_class_id = None
    else:
        print(f"Bottle class ID: {bottle_class_id}")
    
    frame_count = 0
    start_time = time.time()
    bottle_detections = 0
    
    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Error: Could not read camera frame")
                break
            
            frame_count += 1
            
            # Run YOLOv8 detection every 5 frames for better performance
            if frame_count % 5 == 0:
                results = model(frame, verbose=False)
                
                # Process detections
                for result in results:
                    if result.boxes is not None:
                        for box in result.boxes:
                            confidence = box.conf.item()
                            if confidence >= CONFIDENCE_THRESHOLD:
                                class_id = int(box.cls.item())
                                class_name = class_names[class_id]
                                
                                # Filter for bottles only
                                if bottle_class_id is None or class_id == bottle_class_id:
                                    # Get bounding box coordinates
                                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                                    
                                    if class_name.lower() == 'bottle':
                                        bottle_detections += 1
                                        print(f"Bottle detected! (confidence: {confidence:.2f}, position: {int(x1)},{int(y1)}-{int(x2)},{int(y2)})")
                                    else:
                                        print(f"Object detected: {class_name} (confidence: {confidence:.2f})")
            
            # Calculate and display FPS every 30 frames
            if frame_count % 30 == 0:
                elapsed_time = time.time() - start_time
                fps = frame_count / elapsed_time if elapsed_time > 0 else 0
                print(f"FPS: {fps:.1f}, Total bottles detected: {bottle_detections}")
                
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    except Exception as e:
        print(f"Error during bottle detection test: {e}")
    finally:
        # Cleanup
        camera.release()
        print(f"Bottle detection test completed. Total bottles detected: {bottle_detections}")

if __name__ == "__main__":
    test_bottle_detection()

