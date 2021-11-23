import os
import threading

lock = threading.Lock()
exitcode = 0

def reboot():
    os.system(f"sudo systemctl reboot")

def shutdown():
    os.system(f"sudo systemctl poweroff")

def softReboot():
    global exitcode
    with lock:
        exitcode = 10
    exit(10)