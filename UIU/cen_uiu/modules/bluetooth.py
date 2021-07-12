"""
standard dbus interfaces
https://dbus.freedesktop.org/doc/dbus-specification.html#standard-interfaces
"""

import subprocess
import multiprocessing
import re
from typing import List
import dbus
from dbus.exceptions import DBusException
from dbus.proxies import ProxyObject


from kivy.logger import Logger
_LOGGER = Logger

bus = dbus.SystemBus()

AUDIO_SRC = "0000110a-0000-1000-8000-00805f9b34fb"

BL_ON_CONNECT_EVENT = "bl-on-connect"


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
    try:
        properties_interface = dbus.Interface(
            interface, "org.freedesktop.DBus.Properties")

        return properties_interface.Get(interface.dbus_interface, name)
    except DBusException:
        return None


def set_interface_property(interface: dbus.Interface, name: str, value) -> bool:
    try:
        properties_interface = dbus.Interface(
            interface, "org.freedesktop.DBus.Properties")

        properties_interface.Set(interface.dbus_interface, name, value)
    except DBusException:
        return False

    return True


def get_adapter(name: str) -> dbus.Interface:
    """
    https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/adapter-api.txt
    """
    device_proxy_object = get_proxy_object(f"/org/bluez/{name}")
    return dbus.Interface(device_proxy_object, "org.bluez.Adapter1")


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
    return dbus.Interface(device, "org.bluez.MediaPlayer1")


def list_devices() -> List[str]:
    proxy = get_proxy_object("/")
    manager = dbus.Interface(proxy, "org.freedesktop.DBus.ObjectManager")

    objects = manager.GetManagedObjects()

    reg_dev = re.compile("\/org\/bluez\/hci\d*\/dev\_(.*)")
    # e.g., match a string like this:
    # /org/bluez/hci0/dev_58_C9_35_2F_A1_EF

    devices = []

    for key, value in objects.items():
        m = reg_dev.match(key)

        if m is not None:
            dev_str = m.group(1)

            devices.append(dev_str)

    return devices


class BluetoothDiscovery(multiprocessing.Process):
    def __init__(self, core, adapter: str = "hci0") -> None:
        super().__init__(name="bluetooth-worker")
        self._core = core
        self._adapter = adapter

    def run(self):
        adapter = get_adapter(self._adapter)

        set_interface_property(adapter, "Discoverable", True)

        try:
            adapter.StartDiscovery()
        except DBusException:
            pass

        while True:
            for device in list_devices():
                device = get_device(self._adapter, device)

                paired: bool = get_interface_property(device, "Paired")
                connected: bool = get_interface_property(device, "Connected")
                uuids: List[str] = get_interface_property(device, "UUIDs")

                if paired and not connected and uuids.count(AUDIO_SRC) > 0:
                    try:
                        device.ConnectProfile(AUDIO_SRC)
                    except DBusException:
                        continue

                    while not get_interface_property(device, "Connected"):
                        pass

                    self._core.event.call(
                        BL_ON_CONNECT_EVENT, {"device": device})


class BluetoothError(Exception):
    pass
