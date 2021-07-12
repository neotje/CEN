"""
this file is responsible for connecting and discovering bluetooth devices.

standard dbus interfaces
https://dbus.freedesktop.org/doc/dbus-specification.html#standard-interfaces
"""
import re
from typing import List

import dbus
from dbus.exceptions import DBusException
from dbus.proxies import ProxyObject

from cen_uiu.modules.interfaces.adapter_api import BluezAdapter1
from cen_uiu.modules.interfaces.device_api import BluezDevice1

from kivy.logger import Logger
_LOGGER = Logger

# system bus
bus = dbus.SystemBus()

# audio source UUID
AUDIO_SRC = "0000110a-0000-1000-8000-00805f9b34fb"


def get_proxy_object(path: str) -> ProxyObject:
    return bus.get_object("org.bluez", path)


def get_adapter(name: str) -> BluezAdapter1:
    """
    https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/adapter-api.txt
    """
    device_proxy_object = get_proxy_object(f"/org/bluez/{name}")
    return BluezAdapter1(dbus.Interface(device_proxy_object, "org.bluez.Adapter1"))


def get_device(adapter: str, device: str) -> BluezDevice1:
    """
    https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/device-api.txt
    """
    device_proxy_object = get_proxy_object(
        f"/org/bluez/{adapter}/dev_{device}")
    return BluezDevice1(dbus.Interface(device_proxy_object, "org.bluez.Device1"))


def get_media_player(device: dbus.Interface) -> dbus.Interface:
    """
    TODO: create a BluezMediaPlayer1 bus.BusObject
    """
    return dbus.Interface(device, "org.bluez.MediaPlayer1")


def list_devices() -> List[str]:
    """
    TODO: Return list of BluezDevice1
    """
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


def discover_and_connect(core, adapter_str: str, *args):
    _LOGGER.info("Bluetooth: scanning...")
    adapter = get_adapter(adapter_str)

    adapter.Discoverable = True

    try:
        # FIXME: Freezes the kivy app if bluez is not working correctly. (add shorter timeout)
        adapter.StartDiscovery()
    except DBusException:
        pass

    for device in list_devices():
        device = get_device(adapter_str, device)

        paired: bool = device.Paired
        connected: bool = device.Connected
        uuids: List[str] = device.UUIDs

        if paired and not connected and uuids.count(AUDIO_SRC) > 0:
            _LOGGER.info(f"Bluetooth: connecting to {device.object_path}")
            device.ConnectProfile(AUDIO_SRC)

            while not device.Connected:
                pass


class BluetoothError(Exception):
    pass
