import os

def reboot():
    os.system(f"sudo systemctl reboot")

def shutdown():
    os.system(f"sudo systemctl poweroff")

def softReboot():
    exit(10)