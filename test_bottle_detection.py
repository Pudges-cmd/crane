#!/usr/bin/env python3
"""
Bottle Detection Test Script for Raspberry Pi 4B
Tests YOLOv8 detection specifically for bottles.
Optimized for Raspberry Pi performance.
"""

import cv2
import time
import os
from ultralytics import YOLO
from config import *

def test_bottle_detection():
    """Test bottle detection functionality"""
    print("Bottle Detection Test Script")
    print("This will test YOLOv8 detection specifically for bottles")
    print("Press 'q' to quit")
    
    # Initialize camera
    camera = cv2.VideoCapture(CAMERA_INDEX)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    
    if not camera.isOpened():
        print("Error: Could not open camera")
        return
    
    print(f"Camera initialized at {CAMERA_WIDTH}x{CAMERA_HEIGHT}")
    
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
                
                # Draw detections on frame
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
                                    
                                    # Draw bounding box (green for bottles)
                                    color = (0, 255, 0) if class_name.lower() == 'bottle' else (0, 0, 255)
                                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
                                    
                                    # Draw label
                                    label = f"{class_name}: {confidence:.2f}"
                                    cv2.putText(frame, label, (int(x1), int(y1) - 10), 
                                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                                    
                                    if class_name.lower() == 'bottle':
                                        bottle_detections += 1
                                        print(f"Bottle detected! (confidence: {confidence:.2f})")
            
            # Calculate and display FPS
            elapsed_time = time.time() - start_time
            fps = frame_count / elapsed_time if elapsed_time > 0 else 0
            
            # Display stats
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Bottles detected: {bottle_detections}", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Display frame
            cv2.imshow('Bottle Detection Test', frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    except Exception as e:
        print(f"Error during bottle detection test: {e}")
    finally:
        # Cleanup
        camera.release()
        cv2.destroyAllWindows()
        print(f"Bottle detection test completed. Total bottles detected: {bottle_detections}")

if __name__ == "__main__":
    test_bottle_detection()

