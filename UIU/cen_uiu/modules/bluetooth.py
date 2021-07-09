"""
standard dbus interfaces
https://dbus.freedesktop.org/doc/dbus-specification.html#standard-interfaces
"""

import subprocess
import re
from typing import List
import dbus
from dbus.proxies import ProxyObject
from .interfaces.adapter_api import BluezAdapter1

bus = dbus.SystemBus()


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


def get_proxy_object(path: str) -> ProxyObject:
    return bus.get_object("org.bluez", path)


def get_interface_property(interface: dbus.Interface, name: str):
    properties_interface = dbus.Interface(
        interface.proxy_object, "org.freedesktop.DBus.Properties")

    return properties_interface.Get(interface.dbus_interface, name)


def get_adapter(name: str) -> BluezAdapter1:
    return BluezAdapter1(bus, f"/org/bluez/{name}")


def get_agent() -> dbus.Interface:
    """
    https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/agent-api.txt
    """
    device_proxy_object = get_proxy_object("/org/bluez")
    return dbus.Interface(device_proxy_object, "org.bluez.AgentManager1")


def get_device(adapter: str, device: str) -> dbus.Interface:
    """
    https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/device-api.txt
    """
    device_proxy_object = get_proxy_object(
        f"/org/bluez/{adapter}/dev_{device}")
    return dbus.Interface(device_proxy_object, "org.bluez.Device1")


def get_media_player(device: dbus.Interface) -> dbus.Interface:
    return dbus.Interface(device.proxy_object, "org.bluez.MediaPlayer1")


def list_devices() -> List[str]:
    proxy = get_proxy_object("/")
    manager = dbus.Interface(proxy, "org.freedesktop.DBus.ObjectManager")

    objects = manager.GetManagedObjects()

    r = re.compile("\/org\/bluez\/hci\d*\/dev\_(.*)")
    # e.g., match a string like this:
    # /org/bluez/hci0/dev_58_C9_35_2F_A1_EF

    devices = []

    for key, value in objects.items():
        m = r.match(key)

        if m is not None:
            dev_str = m.group(1)
            devices.append(dev_str)

    return devices


class BluetoothError(Exception):
    pass
