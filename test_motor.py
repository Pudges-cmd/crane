#!/usr/bin/env python3
"""
Simple motor test script for Raspberry Pi 4B
Tests basic motor functionality without object detection.
Use this to verify your motor connections before running the full system.
"""

import RPi.GPIO as GPIO
import time
from config import *

def test_motor():
    """Test motor functionality"""
    print("Motor Test Script")
    print("This will test your motor connections")
    print("Press Ctrl+C to stop")
    
    # Setup GPIO
    if GPIO_MODE == "BCM":
        GPIO.setmode(GPIO.BCM)
    else:
        GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(MOTOR_PIN1, GPIO.OUT)
    GPIO.setup(MOTOR_PIN2, GPIO.OUT)
    GPIO.setup(ENABLE_PIN, GPIO.OUT)
    
    # Initialize PWM
    pwm = GPIO.PWM(ENABLE_PIN, 1000)
    pwm.start(0)
    
    try:
        print(f"Testing motor with pins: {MOTOR_PIN1}, {MOTOR_PIN2}, {ENABLE_PIN}")
        
        # Test different speeds
        for speed in [25, 50, 75, 100]:
            print(f"Testing motor at {speed}% speed...")
            
            # Start motor
            GPIO.output(MOTOR_PIN1, GPIO.HIGH)
            GPIO.output(MOTOR_PIN2, GPIO.LOW)
            pwm.ChangeDutyCycle(speed)
            
            # Run for 3 seconds
            time.sleep(3)
            
            # Stop motor
            GPIO.output(MOTOR_PIN1, GPIO.LOW)
            GPIO.output(MOTOR_PIN2, GPIO.LOW)
            pwm.ChangeDutyCycle(0)
            
            print(f"Motor test at {speed}% completed")
            time.sleep(1)
        
        print("All motor tests completed successfully!")
        
    except KeyboardInterrupt:
        print("\nTest stopped by user")
    except Exception as e:
        print(f"Error during motor test: {e}")
    finally:
        # Cleanup
        pwm.stop()
        GPIO.cleanup()
        print("GPIO cleanup completed")

if __name__ == "__main__":
    test_motor()
