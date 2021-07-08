import subprocess

def discoverable(enable: bool = True):
    if enable:
        subprocess.run(["bluetoothctl", "discoverable", "on"])
    else:
        subprocess.run(["bluetoothctl", "discoverable", "off"])

def set_alias(alias: str):
    result = subprocess.run(["bluetoothctl", "system-alias", alias])

    if result.returncode is not 0:
        raise BluetoothError


class BluetoothError(Exception):
    pass