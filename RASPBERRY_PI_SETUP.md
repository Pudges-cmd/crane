# Raspberry Pi 4B Setup Guide

## Quick Setup for Bottle Detection

### 1. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3-pip python3-opencv git

# Install Python packages
pip3 install -r requirements.txt
```

### 2. Enable Camera

```bash
# Enable camera in raspi-config
sudo raspi-config
# Navigate to: Interface Options > Camera > Enable
# Reboot when prompted
```

### 3. Detect Available Cameras

```bash
# Detect and list available cameras (USB, Pi Camera)
python3 camera_detector.py
```

### 4. Test Camera

```bash
# Test camera functionality
python3 test_camera.py
```

### 5. Test Bottle Detection

```bash
# Test bottle detection specifically (auto-detects cameras)
python3 test_bottle_detection_headless.py
```

### 6. Run Motor Control

```bash
# Run the main motor control with bottle detection
python3 motor_control.py
```

## Hardware Setup

1. Connect motor driver to GPIO pins:
   - Motor Pin 1: GPIO 17
   - Motor Pin 2: GPIO 18  
   - Enable Pin: GPIO 27

2. Connect camera module or USB camera

3. Power up the system

## Configuration

Edit `config.py` to adjust settings:

```python
# Motor speed (0-100)
MOTOR_SPEED = 50

# Detection sensitivity (0.0-1.0)
CONFIDENCE_THRESHOLD = 0.5

# Camera resolution
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
```

## Troubleshooting

### Camera Issues
```bash
# Check camera status
vcgencmd get_camera

# List USB devices
lsusb

# Detect available cameras
python3 camera_detector.py
```

### USB Camera Setup
1. **Connect USB camera** to any USB port
2. **Check if detected**: `lsusb | grep -i camera`
3. **Find camera index**: `python3 camera_detector.py`
4. **Update config.py** with the correct CAMERA_INDEX
5. **Test camera**: `python3 test_bottle_detection_headless.py`

### Performance Issues
- Reduce camera resolution in `config.py`
- Increase `DETECTION_INTERVAL` for slower detection
- Use a USB camera instead of Pi Camera for better performance

### GPIO Issues
```bash
# Check GPIO permissions
groups $USER

# Add user to gpio group if needed
sudo usermod -a -G gpio $USER
# Log out and back in
```

