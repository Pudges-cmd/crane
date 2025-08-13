#!/usr/bin/env python3
"""
Raspberry Pi 4B Motor Control with YOLOv5 Object Detection (Configurable Version)
Controls a motor continuously until an object is detected, then stops the motor.
Uses configuration file for easy customization.
"""

import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import threading
from ultralytics import YOLO
import os
import logging
from config import *

class MotorController:
    def __init__(self, motor_pin1=MOTOR_PIN1, motor_pin2=MOTOR_PIN2, enable_pin=ENABLE_PIN):
        """
        Initialize motor controller with GPIO pins from config
        
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
        
        # Setup GPIO based on config
        if GPIO_MODE == "BCM":
            GPIO.setmode(GPIO.BCM)
        else:
            GPIO.setmode(GPIO.BOARD)
            
        GPIO.setup(self.motor_pin1, GPIO.OUT)
        GPIO.setup(self.motor_pin2, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        
        # Initialize PWM for speed control
        self.pwm = GPIO.PWM(self.enable_pin, 1000)  # 1kHz frequency
        self.pwm.start(0)
        
        logging.info("Motor controller initialized")
        print("Motor controller initialized")
    
    def start_motor(self, speed=MOTOR_SPEED):
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
            logging.info(f"Motor started at {speed}% speed")
            print(f"Motor started at {speed}% speed")
    
    def stop_motor(self):
        """Stop the motor"""
        if self.is_running:
            GPIO.output(self.motor_pin1, GPIO.LOW)
            GPIO.output(self.motor_pin2, GPIO.LOW)
            self.pwm.ChangeDutyCycle(0)
            self.is_running = False
            logging.info("Motor stopped")
            print("Motor stopped")
    
    def cleanup(self):
        """Clean up GPIO resources"""
        self.stop_motor()
        if self.pwm:
            self.pwm.stop()
        GPIO.cleanup()
        logging.info("GPIO cleanup completed")
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
        
        # Load YOLOv5 model with error handling
        try:
            if model_path and os.path.exists(model_path):
                self.model = YOLO(model_path)
                logging.info(f"Loaded custom model: {model_path}")
            else:
                # Use default YOLOv5n model
                self.model = YOLO('yolov5n.pt')
                logging.info("Using default YOLOv5n model")
                print("Using default YOLOv5n model")
        except Exception as e:
            logging.error(f"Error loading YOLOv5 model: {e}")
            print(f"Error loading model: {e}")
            raise RuntimeError(f"Failed to load YOLOv5 model: {e}")
        
        # Initialize camera with error handling
        try:
            self.camera = cv2.VideoCapture(CAMERA_INDEX)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
            
            if not self.camera.isOpened():
                logging.error("Could not open camera")
                print("Error: Could not open camera")
                raise RuntimeError("Camera not available")
                
            # Test camera by reading a frame
            ret, test_frame = self.camera.read()
            if not ret:
                logging.error("Could not read from camera")
                print("Error: Could not read from camera")
                raise RuntimeError("Camera not responding")
                
        except Exception as e:
            logging.error(f"Camera initialization error: {e}")
            print(f"Camera error: {e}")
            raise RuntimeError(f"Failed to initialize camera: {e}")
        
        logging.info("Object detector initialized")
        print("Object detector initialized")
    
    def detect_objects(self):
        """
        Detect objects in the current camera frame
        
        Returns:
            bool: True if objects detected, False otherwise
        """
        ret, frame = self.camera.read()
        if not ret:
            logging.error("Could not read camera frame")
            print("Error: Could not read camera frame")
            return False
        
        try:
            # Run YOLOv5 detection with error handling
            results = self.model(frame, verbose=False, conf=self.confidence_threshold)
            
            # Check for detections above confidence threshold
            for result in results:
                if result.boxes is not None and len(result.boxes) > 0:
                    for box in result.boxes:
                        confidence = float(box.conf.item())
                        class_id = int(box.cls.item())
                        class_name = self.model.names[class_id]
                        
                        # Check if we should detect this specific class
                        if not self.target_classes or class_name in self.target_classes:
                            logging.info(f"Object detected: {class_name} (confidence: {confidence:.2f})")
                            print(f"Object detected: {class_name} (confidence: {confidence:.2f})")
                            return True
            
            return False
            
        except Exception as e:
            logging.error(f"Error during object detection: {e}")
            print(f"Detection error: {e}")
            return False
    
    def release(self):
        """Release camera resources"""
        if self.camera:
            self.camera.release()

def setup_logging():
    """Setup logging configuration"""
    if ENABLE_LOGGING:
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('motor_control.log'),
                logging.StreamHandler()
            ]
        )

def main():
    """Main function to run motor control with object detection"""
    # Setup logging
    setup_logging()
    
    logging.info("Starting Raspberry Pi Motor Control with YOLOv5 Object Detection")
    print("Starting Raspberry Pi Motor Control with YOLOv5 Object Detection")
    print("Press Ctrl+C to stop")
    
    # Initialize motor controller and object detector
    motor = MotorController()
    detector = ObjectDetector()
    
    try:
        # Start motor
        motor.start_motor()
        
        # Main detection loop
        while True:
            # Check for objects
            if detector.detect_objects():
                logging.info("Object detected! Stopping motor...")
                print("Object detected! Stopping motor...")
                motor.stop_motor()
                break
            
            # Small delay to prevent excessive CPU usage
            time.sleep(DETECTION_INTERVAL)
            
    except KeyboardInterrupt:
        logging.info("Program stopped by user")
        print("\nStopping program...")
    except Exception as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")
    finally:
        # Cleanup
        motor.cleanup()
        detector.release()
        logging.info("Program terminated")
        print("Program terminated")

if __name__ == "__main__":
    main()
