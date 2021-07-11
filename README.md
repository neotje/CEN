[![CCU build](https://github.com/neotje/CEN/actions/workflows/ccu.yml/badge.svg)](https://github.com/neotje/CEN/actions/workflows/ccu.yml)
[![I2C-sm build](https://github.com/neotje/CEN/actions/workflows/I2C-sm.yml/badge.svg)](https://github.com/neotje/CEN/actions/workflows/I2C-sm.yml)

# CEN
Car electronics network (needs a better name i think)

This is my attempt to modernize a Chevrolet Matiz with sensors and a multimedia center.

Features:
 - parking sensors
 - multimedia center with touchscreen
 - over the air updates

## File structure
```
.
+-- CCU (Central Computer unit aka Teensy 4.1 platformio project files)
|   +-- src
|       +-- I2C-sm (Code to send and recieve data from sensor modules)
|       +-- serial-UIU (Serial communication interface)
+-- I2C-sm (I2C Sensor Module aka Arduino Nano platformio project files)
+-- UIU (User Interface Unit aka raspberry pi 4 with a touchscreen)
    +-- scripts (startup scripts)
```
