# Raspberry Pi 4B Motor Control with YOLOv8 Bottle Detection

This project controls a DC motor continuously until it detects a bottle using YOLOv8, then stops the motor. Perfect for automated bottle sorting or recycling systems that need to respond to visual stimuli.

## Features

- **Continuous Motor Control**: Motor spins continuously until bottle detection
- **YOLOv8 Bottle Detection**: Real-time bottle detection using computer vision
- **Optimized for Raspberry Pi**: Uses YOLOv8n model for optimal performance
- **Configurable Settings**: Easy customization through config file
- **PWM Speed Control**: Adjustable motor speed
- **Logging System**: Comprehensive logging for debugging
- **GPIO Safety**: Proper GPIO cleanup and error handling

## Hardware Requirements

- Raspberry Pi 4B/5 (2GB RAM minimum, 4GB+ recommended)
- DC Motor (12V recommended)
- L298N Motor Driver Module (or L293D, TB6612FNG)
- 12V Power Supply for Motor
- Camera Module (Pi Camera v3 or USB camera)
- Breadboard and jumper wires
- MicroSD card (16GB+ recommended, Class 10+)
- Optional: Cooling fan for extended operation

## Software Requirements

- Raspberry Pi OS (Bookworm or newer)
- Python 3.9+
- Camera enabled in raspi-config (or automatically detected)

## Installation

### Quick Setup (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd Crane

# Run the automated setup script
python3 setup.py
```

### Manual Installation

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd Crane
```

#### 2. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3-pip python3-opencv libatlas-base-dev git build-essential cmake pkg-config

# Install Python packages
pip3 install -r requirements.txt
```

#### 3. Enable Camera (if needed)

Modern Raspberry Pi OS automatically detects cameras, but if you need to manually enable:

```bash
# For Pi Camera (usually auto-detected)
sudo raspi-config
# Navigate to: Interface Options > Camera > Enable
# Reboot when prompted

# For USB cameras (usually plug-and-play)
# No additional setup needed
```

#### 4. Configure Hardware

1. Follow the wiring diagram in `wiring_diagram.md`
2. Connect the motor driver to the Raspberry Pi
3. Connect the camera module
4. Power up the system

## Configuration

Edit `config.py` to customize the behavior:

```python
# Motor Configuration
MOTOR_PIN1 = 17      # GPIO pin for motor direction 1
MOTOR_PIN2 = 18      # GPIO pin for motor direction 2
ENABLE_PIN = 27      # GPIO pin for motor enable/PWM
MOTOR_SPEED = 50     # Motor speed (0-100)

# Object Detection Configuration
CONFIDENCE_THRESHOLD = 0.5    # Detection sensitivity
MODEL_PATH = None             # Path to custom model (None for default YOLOv8n)
TARGET_CLASSES = ["bottle"]   # Specific objects to detect (bottles only)
```

## Usage

### Basic Usage

```bash
# Run the basic version
python3 motor_control.py

# Run the configurable version (recommended)
python3 motor_control_config.py
```

### Manual Motor Control

For manual control of the motor direction:

```bash
# Advanced manual control (arrow keys)
python3 manual_motor_control.py

# Simple manual control (WASD keys)
python3 manual_motor_control_simple.py
```

**Manual Control Commands:**
- **Arrow Keys** (advanced): ↑ Clockwise, ↓ Counterclockwise, Space Stop
- **WASD Keys** (simple): W Clockwise, S Counterclockwise, X Stop
- **Speed Control**: + Increase speed, - Decrease speed
- **Quit**: Q

### Bottle Detection Testing

Test the bottle detection system specifically:

```bash
# Test bottle detection with camera feed
python3 test_bottle_detection.py

# Test general camera and detection
python3 test_camera.py
```

The bottle detection test will:
- Load the YOLOv8n model (automatically downloaded on first run)
- Filter detections to show only bottles
- Display real-time detection results
- Show confidence scores for detected bottles

### Custom Object Detection

To detect specific objects only, edit `config.py`:

```python
TARGET_CLASSES = ["person", "car", "bottle"]  # Only detect these objects
```

### Custom YOLOv5 Model

Place your custom model file in the project directory and update `config.py`:

```python
MODEL_PATH = "path/to/your/custom_model.pt"
```

## How It Works

1. **Initialization**: The system initializes the motor controller and YOLOv5 object detector
2. **Motor Start**: The motor begins spinning at the configured speed
3. **Object Detection**: The camera continuously captures frames and runs YOLOv5 detection
4. **Detection Logic**: When an object is detected above the confidence threshold, the motor stops
5. **Cleanup**: GPIO pins are properly cleaned up on exit

## File Structure

```
Crane/
├── setup.py                      # Automated setup script
├── motor_control.py              # Main motor control with bottle detection
├── motor_control_config.py       # Configurable version (recommended)
├── manual_motor_control.py       # Manual control with arrow keys
├── manual_motor_control_simple.py # Manual control with WASD keys
├── test_motor.py                 # Motor testing script
├── test_camera.py                # Camera testing script
├── test_bottle_detection.py      # Bottle detection test script
├── config.py                     # Configuration settings
├── requirements.txt              # Python dependencies
├── wiring_diagram.md             # Hardware setup guide
└── README.md                     # This file
```

## Troubleshooting

### Common Issues

1. **GPIO Permission Error**
   ```bash
   # Modern Raspberry Pi OS handles GPIO permissions automatically
   # If you still get permission errors:
   sudo usermod -a -G gpio $USER
   # Log out and back in
   
   # Alternative: Run with sudo (not recommended for production)
   sudo python3 motor_control_config.py
   ```

2. **Camera Not Detected**
   ```bash
   # Check camera status
   vcgencmd get_camera
   
   # List USB devices
   lsusb
   
   # Check camera modules
   lsmod | grep camera
   
   # Enable camera in raspi-config (if needed)
   sudo raspi-config
   ```

3. **Motor Not Spinning**
   - Check power supply connections
   - Verify GPIO pin assignments
   - Test motor driver with multimeter

4. **YOLOv5 Model Download Issues**
   ```bash
   # Manual download (latest version)
   wget https://github.com/ultralytics/assets/releases/download/v8.0.0/yolov5n.pt
   
   # Or use ultralytics to download
   python3 -c "from ultralytics import YOLO; YOLO('yolov5n.pt')"
   ```

5. **Performance Issues**
   - Reduce camera resolution in config
   - Increase detection interval
   - Use smaller YOLOv5 model (yolov5n instead of yolov5s)

### Performance Optimization

For better performance on Raspberry Pi:

1. **Use YOLOv5n**: Smallest and fastest model
2. **Reduce Resolution**: Lower camera resolution for faster processing
3. **Increase Detection Interval**: Longer delays between detections
4. **Enable GPU acceleration**: 
   ```bash
   # Enable OpenGL driver
   sudo raspi-config
   # Advanced Options > GL Driver > GL (Full KMS)
   ```
5. **Overclock**: Enable overclocking in raspi-config (use with caution)
6. **Use SSD**: Boot from USB SSD for faster I/O

## Safety Considerations

1. **Electrical Safety**: Never connect motor power directly to GPIO pins
2. **Mechanical Safety**: Secure motor mounting to prevent accidents
3. **Power Supply**: Use appropriate power supplies for your motor
4. **Heat Management**: Monitor Raspberry Pi temperature during operation

## Customization Ideas

- **Multiple Motors**: Extend the code to control multiple motors
- **Direction Control**: Add reverse direction capability
- **Speed Variation**: Implement variable speed based on object distance
- **Web Interface**: Add web-based control and monitoring
- **Data Logging**: Log detection events and motor operation
- **Alert System**: Add email/SMS notifications on object detection
- **Mobile App**: Create a mobile app for remote control
- **AI Training**: Train custom YOLOv5 models for specific objects
- **IoT Integration**: Connect to home automation systems

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project.

## License

This project is open source and available under the MIT License.

## Support

For support and questions:
- Check the troubleshooting section
- Review the wiring diagram
- Test individual components separately
- Check system logs for error messages
