#!/usr/bin/env python3
"""
Manual Motor Control for Raspberry Pi 4B
Controls motor direction using keyboard input:
- Up Arrow: Clockwise rotation
- Down Arrow: Counterclockwise rotation
- Space: Stop motor
- Q: Quit program
"""

import RPi.GPIO as GPIO
import time
import sys
import tty
import termios
from config import *

class ManualMotorController:
    def __init__(self, motor_pin1=MOTOR_PIN1, motor_pin2=MOTOR_PIN2, enable_pin=ENABLE_PIN):
        """
        Initialize manual motor controller with GPIO pins from config
        
        Args:
            motor_pin1 (int): GPIO pin for motor direction 1
            motor_pin2 (int): GPIO pin for motor direction 2  
            enable_pin (int): GPIO pin for motor enable/PWM
        """
        self.motor_pin1 = motor_pin1
        self.motor_pin2 = motor_pin2
        self.enable_pin = enable_pin
        self.is_running = False
        self.current_direction = "stopped"
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
        
        print("Manual motor controller initialized")
        print(f"Using pins: {motor_pin1}, {motor_pin2}, {enable_pin}")
    
    def rotate_clockwise(self, speed=MOTOR_SPEED):
        """Rotate motor clockwise"""
        GPIO.output(self.motor_pin1, GPIO.HIGH)
        GPIO.output(self.motor_pin2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(speed)
        self.is_running = True
        self.current_direction = "clockwise"
        print(f"Motor rotating CLOCKWISE at {speed}% speed")
    
    def rotate_counterclockwise(self, speed=MOTOR_SPEED):
        """Rotate motor counterclockwise"""
        GPIO.output(self.motor_pin1, GPIO.LOW)
        GPIO.output(self.motor_pin2, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(speed)
        self.is_running = True
        self.current_direction = "counterclockwise"
        print(f"Motor rotating COUNTERCLOCKWISE at {speed}% speed")
    
    def stop_motor(self):
        """Stop the motor"""
        GPIO.output(self.motor_pin1, GPIO.LOW)
        GPIO.output(self.motor_pin2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)
        self.is_running = False
        self.current_direction = "stopped"
        print("Motor STOPPED")
    
    def change_speed(self, speed):
        """Change motor speed while maintaining direction"""
        if self.is_running:
            self.pwm.ChangeDutyCycle(speed)
            print(f"Speed changed to {speed}%")
    
    def get_status(self):
        """Get current motor status"""
        return {
            "running": self.is_running,
            "direction": self.current_direction,
            "speed": self.pwm._dutycycle if self.pwm else 0
        }
    
    def cleanup(self):
        """Clean up GPIO resources"""
        self.stop_motor()
        if self.pwm:
            self.pwm.stop()
        GPIO.cleanup()
        print("GPIO cleanup completed")

def get_key():
    """Get a single keypress from the user"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def print_instructions():
    """Print control instructions"""
    print("\n" + "="*50)
    print("MANUAL MOTOR CONTROL")
    print("="*50)
    print("Controls:")
    print("  ↑ (Up Arrow)    : Rotate CLOCKWISE")
    print("  ↓ (Down Arrow)  : Rotate COUNTERCLOCKWISE")
    print("  SPACE           : STOP motor")
    print("  +               : Increase speed")
    print("  -               : Decrease speed")
    print("  Q               : Quit program")
    print("="*50)
    print("Current Status: Motor stopped")
    print("="*50)

def main():
    """Main function for manual motor control"""
    print("Starting Manual Motor Control")
    print("Press Ctrl+C to stop")
    
    # Initialize motor controller
    motor = ManualMotorController()
    current_speed = MOTOR_SPEED
    
    try:
        print_instructions()
        
        while True:
            # Get keypress
            key = get_key()
            
            if key == '\x1b[A':  # Up arrow
                motor.rotate_clockwise(current_speed)
            elif key == '\x1b[B':  # Down arrow
                motor.rotate_counterclockwise(current_speed)
            elif key == ' ':  # Space
                motor.stop_motor()
            elif key == '+':  # Increase speed
                current_speed = min(100, current_speed + 10)
                if motor.is_running:
                    motor.change_speed(current_speed)
                print(f"Speed set to {current_speed}%")
            elif key == '-':  # Decrease speed
                current_speed = max(10, current_speed - 10)
                if motor.is_running:
                    motor.change_speed(current_speed)
                print(f"Speed set to {current_speed}%")
            elif key.lower() == 'q':  # Quit
                print("\nQuitting...")
                break
            elif key == '\x03':  # Ctrl+C
                print("\nInterrupted by user")
                break
            
            # Small delay to prevent excessive CPU usage
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nStopping program...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup
        motor.cleanup()
        print("Program terminated")

if __name__ == "__main__":
    main()
