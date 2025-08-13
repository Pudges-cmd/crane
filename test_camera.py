#!/usr/bin/env python3
"""
Camera and YOLOv5 test script for Raspberry Pi 4B
Tests camera functionality and object detection without motor control.
Use this to verify your camera setup before running the full system.
"""

import cv2
import time
from ultralytics import YOLO
from config import *

def test_camera():
    """Test camera functionality"""
    print("Camera Test Script")
    print("This will test your camera and YOLOv5 detection")
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
    
    frame_count = 0
    start_time = time.time()
    
    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                print("Error: Could not read camera frame")
                break
            
            frame_count += 1
            
            # Run YOLOv8 detection every 10 frames for performance
            if frame_count % 10 == 0:
                results = model(frame, verbose=False)
                
                # Draw detections on frame
                for result in results:
                    if result.boxes is not None:
                        for box in result.boxes:
                            confidence = box.conf.item()
                            if confidence >= CONFIDENCE_THRESHOLD:
                                class_id = int(box.cls.item())
                                class_name = model.names[class_id]
                                
                                # Check if we should detect this specific class
                                if not TARGET_CLASSES or class_name in TARGET_CLASSES:
                                    # Get bounding box coordinates
                                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                                    
                                    # Draw bounding box
                                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                                    
                                    # Draw label
                                    label = f"{class_name}: {confidence:.2f}"
                                    cv2.putText(frame, label, (int(x1), int(y1) - 10), 
                                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                    
                                    print(f"Object detected: {class_name} (confidence: {confidence:.2f})")
            
            # Calculate and display FPS
            elapsed_time = time.time() - start_time
            fps = frame_count / elapsed_time if elapsed_time > 0 else 0
            
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Display frame
            cv2.imshow('Camera Test', frame)
            
            # Check for quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    except Exception as e:
        print(f"Error during camera test: {e}")
    finally:
        # Cleanup
        camera.release()
        cv2.destroyAllWindows()
        print("Camera test completed")

if __name__ == "__main__":
    test_camera()
