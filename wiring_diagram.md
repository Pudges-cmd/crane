# Raspberry Pi 4B Motor Control Wiring Diagram

## Hardware Requirements

- Raspberry Pi 4B
- DC Motor (12V recommended)
- L298N Motor Driver Module
- 12V Power Supply for Motor
- Camera Module (Pi Camera or USB camera)
- Breadboard and jumper wires
- Optional: Motor mounting bracket

## Wiring Connections

### L298N Motor Driver to Raspberry Pi

| L298N Pin | Raspberry Pi GPIO | Description |
|-----------|------------------|-------------|
| ENA       | GPIO 27          | Enable A (PWM for speed control) |
| IN1       | GPIO 17          | Input 1 (Direction control) |
| IN2       | GPIO 18          | Input 2 (Direction control) |
| VCC       | 5V               | Logic power supply |
| GND       | GND              | Ground |

### L298N Motor Driver to Motor

| L298N Pin | Motor Connection | Description |
|-----------|------------------|-------------|
| OUT1      | Motor Terminal 1 | Motor output 1 |
| OUT2      | Motor Terminal 2 | Motor output 2 |
| 12V       | 12V Power Supply | Motor power supply |
| GND       | 12V Power Supply GND | Motor power ground |

### Camera Connection

- **Pi Camera**: Connect to CSI port on Raspberry Pi
- **USB Camera**: Connect to any USB port

## Pin Layout (BCM Mode)

```
Raspberry Pi 4B GPIO Layout (BCM):

    3.3V    1  2  5V
 GPIO 2     3  4  5V
 GPIO 3     5  6  GND
 GPIO 4     7  8  GPIO 14
    GND     9  10 GPIO 15
GPIO 17    11  12 GPIO 18
GPIO 27    13  14 GND
GPIO 22    15  16 GPIO 23
    3.3V   17  18 GPIO 24
GPIO 10    19  20 GND
 GPIO 9    21  22 GPIO 25
GPIO 11    23  24 GPIO 8
    GND    25  26 GPIO 7
 GPIO 0    27  28 GPIO 1
 GPIO 5    29  30 GND
 GPIO 6    31  32 GPIO 12
GPIO 13    33  34 GND
GPIO 19    35  36 GPIO 16
GPIO 26    37  38 GPIO 20
    GND    39  40 GPIO 21
```

## Power Supply Requirements

- **Raspberry Pi**: 5V/3A via USB-C
- **Motor**: 12V power supply (current depends on motor specifications)
- **L298N**: Powered by 12V supply, logic powered by Pi 5V

## Safety Notes

1. **Never connect motor power directly to Raspberry Pi GPIO pins**
2. **Use separate power supplies for logic and motor circuits**
3. **Connect grounds together between power supplies**
4. **Use appropriate current-limiting resistors if needed**
5. **Test connections with multimeter before powering on**

## Alternative Motor Drivers

If you don't have an L298N, you can use:
- L293D (similar functionality)
- TB6612FNG (more efficient)
- DRV8833 (compact dual H-bridge)

## Troubleshooting

1. **Motor not spinning**: Check power supply and connections
2. **Motor spinning wrong direction**: Swap motor terminal connections
3. **GPIO errors**: Ensure proper pin configuration in code
4. **Camera not detected**: Check camera connections and enable camera in raspi-config
