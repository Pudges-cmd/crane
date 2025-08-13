#!/usr/bin/env python3
"""
Raspberry Pi 4B Motor Control with YOLOv5 Object Detection
Controls a motor continuously until a bottle is detected, then stops the motor.
"""

import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import threading
from ultralytics import YOLO
import os
from config import *

class MotorController:
    def __init__(self, motor_pin1=MOTOR_PIN1, motor_pin2=MOTOR_PIN2, enable_pin=ENABLE_PIN):
        """
        Initialize motor controller with GPIO pins
        
        Args:
            motor_pin1 (int): GPIO pin for motor direction 1
            motor_pin2 (int): GPIO pin for motor direction 2  
            enable_pin (int): GPIO pin for motor enable/PWM
        """
        self.motor_pin1 = motor_pin1
        self.motor_pin2 = motor_pin2
        self.enable_pin = enable_pin
        self.is_running = False
        self.pwm = None
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motor_pin1, GPIO.OUT)
        GPIO.setup(self.motor_pin2, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        
        # Initialize PWM for speed control
        self.pwm = GPIO.PWM(self.enable_pin, 1000)  # 1kHz frequency
        self.pwm.start(0)
        
        print("Motor controller initialized")
    
    def start_motor(self, speed=50):
        """
        Start the motor spinning
        
        Args:
            speed (int): Motor speed (0-100)
        """
        if not self.is_running:
            GPIO.output(self.motor_pin1, GPIO.HIGH)
            GPIO.output(self.motor_pin2, GPIO.LOW)
            self.pwm.ChangeDutyCycle(speed)
            self.is_running = True
            print(f"Motor started at {speed}% speed")
    
    def stop_motor(self):
        """Stop the motor"""
        if self.is_running:
            GPIO.output(self.motor_pin1, GPIO.LOW)
            GPIO.output(self.motor_pin2, GPIO.LOW)
            self.pwm.ChangeDutyCycle(0)
            self.is_running = False
            print("Motor stopped")
    
    def cleanup(self):
        """Clean up GPIO resources"""
        self.stop_motor()
        if self.pwm:
            self.pwm.stop()
        GPIO.cleanup()
        print("GPIO cleanup completed")

class ObjectDetector:
    def __init__(self, model_path=MODEL_PATH, confidence_threshold=CONFIDENCE_THRESHOLD):
        """
        Initialize YOLOv5 object detector
        
        Args:
            model_path (str): Path to YOLOv5 model file
            confidence_threshold (float): Minimum confidence for detection
        """
        self.confidence_threshold = confidence_threshold
        self.target_classes = TARGET_CLASSES
        
        # Load YOLOv8 model
        if model_path and os.path.exists(model_path):
            self.model = YOLO(model_path)
            print(f"Loaded local model: {model_path}")
        else:
            # Use default YOLOv8n model
            self.model = YOLO('yolov8n.pt')
            print("Using default YOLOv8n model")
        
        # Initialize camera with auto-detection
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
        
        self.camera = cv2.VideoCapture(camera_index)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        
        if not self.camera.isOpened():
            print(f"Error: Could not open camera at index {camera_index}")
            print("Try running 'python3 camera_detector.py' to find available cameras")
            raise RuntimeError("Camera not available")
        
        print(f"Object detector initialized with camera at index {camera_index}, resolution: {CAMERA_WIDTH}x{CAMERA_HEIGHT}")
        print(f"Target classes: {self.target_classes}")
    
    def detect_objects(self):
        """
        Detect objects in the current camera frame
        
        Returns:
            bool: True if target objects (bottles) detected, False otherwise
        """
        ret, frame = self.camera.read()
        if not ret:
            print("Error: Could not read camera frame")
            return False
        
        # Run YOLOv8 detection
        results = self.model(frame, verbose=False)
        
        # Check for detections above confidence threshold
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    confidence = box.conf.item()
                    if confidence >= self.confidence_threshold:
                        class_id = int(box.cls.item())
                        class_name = self.model.names[class_id]
                        
                        # Check if this is a target class (bottle)
                        if not self.target_classes or class_name in self.target_classes:
                            print(f"Target object detected: {class_name} (confidence: {confidence:.2f})")
                            return True
        
        return False
    
    def release(self):
        """Release camera resources"""
        if self.camera:
            self.camera.release()

def main():
    """Main function to run motor control with bottle detection"""
    print("Starting Raspberry Pi Motor Control with YOLOv5 Bottle Detection")
    print("Motor will run until a bottle is detected")
    print("Press Ctrl+C to stop")
    
    # Initialize motor controller and object detector
    motor = MotorController()
    detector = ObjectDetector()
    
    try:
        # Start motor
        motor.start_motor(speed=MOTOR_SPEED)
        
        # Main detection loop
        while True:
            # Check for bottles
            if detector.detect_objects():
                print("Bottle detected! Stopping motor...")
                motor.stop_motor()
                break
            
            # Small delay to prevent excessive CPU usage
            time.sleep(DETECTION_INTERVAL)
            
    except KeyboardInterrupt:
        print("\nStopping program...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        motor.cleanup()
        detector.release()
        print("Program terminated")

if __name__ == "__main__":
    main()
