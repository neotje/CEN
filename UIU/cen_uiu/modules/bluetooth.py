import subprocess


def discoverable(enable: bool = True):
    if enable:
        result = subprocess.run(["bluetoothctl", "discoverable", "on"])
    else:
        result = subprocess.run(["bluetoothctl", "discoverable", "off"])

    if result.returncode != 0:
        raise BluetoothError

    return True


def set_alias(alias: str):
    result = subprocess.run(["bluetoothctl", "system-alias", alias])

    if result.returncode != 0:
        raise BluetoothError

    return True


class BluetoothError(Exception):
    pass
