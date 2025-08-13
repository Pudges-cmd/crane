"""
Configuration file for Raspberry Pi Motor Control with YOLOv5
Adjust these settings according to your hardware setup and requirements.
"""

# Motor Configuration
MOTOR_PIN1 = 17      # GPIO pin for motor direction 1
MOTOR_PIN2 = 18      # GPIO pin for motor direction 2
ENABLE_PIN = 27      # GPIO pin for motor enable/PWM
MOTOR_SPEED = 50     # Motor speed (0-100)

# Object Detection Configuration
CONFIDENCE_THRESHOLD = 0.5    # Minimum confidence for object detection (0.0-1.0)
MODEL_PATH = "yolov8n.pt"     # Path to local YOLOv8n model
DETECTION_INTERVAL = 0.1      # Time between detections in seconds

# Camera Configuration
CAMERA_INDEX = 1              # Camera device index (0=Pi Camera, 1=USB Camera, 2=USB Camera 2, etc.)
CAMERA_WIDTH = 640            # Camera resolution width
CAMERA_HEIGHT = 480           # Camera resolution height
CAMERA_AUTO_DETECT = True     # Auto-detect available cameras

# GPIO Configuration
GPIO_MODE = "BCM"             # GPIO mode: "BCM" or "BOARD"

# Detection Classes (optional - for specific object detection)
# Leave empty to detect all objects, or specify class names to detect only certain objects
TARGET_CLASSES = ["bottle"]   # Filter to detect only bottles

# Logging Configuration
ENABLE_LOGGING = True         # Enable/disable logging
LOG_LEVEL = "INFO"           # Log level: DEBUG, INFO, WARNING, ERROR
