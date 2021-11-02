import os


ACTUAL_BRIGHTNESS = "/sys/class/backlight/rpi_backlight/actual_brightness"

def getBrightness() -> int:
    with open(ACTUAL_BRIGHTNESS) as file:
        return int(file.read())

def setBrightness(level: int):
    level = min(255, max(0, level))

    os.system(f"sudo sh -c 'echo \"{level}\" > /sys/class/backlight/rpi_backlight/brightness'")