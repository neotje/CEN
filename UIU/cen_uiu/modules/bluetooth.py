"""
this file is responsible for connecting and discovering bluetooth devices.

standard dbus interfaces
https://dbus.freedesktop.org/doc/dbus-specification.html#standard-interfaces
"""
import re
from typing import List
from cen_uiu.modules.dbus import get_proxy_object

import dbus
from dbus.exceptions import DBusException

from cen_uiu.modules.interfaces.adapter_api import BluezAdapter1
from cen_uiu.modules.interfaces.device_api import BluezDevice1

import logging
Logger = logging.getLogger(__name__)
_LOGGER = Logger

# audio source UUID
AUDIO_SRC = "0000110a-0000-1000-8000-00805f9b34fb"


def get_adapter(name: str) -> BluezAdapter1:
    """
    https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/adapter-api.txt
    """
    device_proxy_object = get_proxy_object(f"/org/bluez/{name}")
    return BluezAdapter1(device_proxy_object)


def get_device(adapter: str, device: str) -> BluezDevice1:
    """
    https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/device-api.txt
    """
    device_proxy_object = get_proxy_object(
        f"/org/bluez/{adapter}/dev_{device}")
    return BluezDevice1(device_proxy_object)


def get_media_transport(device):
    pass


def list_devices() -> List[BluezDevice1]:
    proxy = get_proxy_object("/")
    manager = dbus.Interface(proxy, "org.freedesktop.DBus.ObjectManager")

    # TODO: ObjectManager interface
    objects = manager.GetManagedObjects()

    reg_dev = re.compile("\/org\/bluez\/hci\d*\/dev\_(.*)")
    # e.g., match a string like this:
    # /org/bluez/hci0/dev_58_C9_35_2F_A1_EF

    devices: List[BluezDevice1] = []

    for key, value in objects.items():
        m = reg_dev.match(key)

        if m is not None:
            dev_str = m.group(1)

            devices.append(get_device("hci0", dev_str))

    return devices


def list_connected_devices() -> List[BluezDevice1]:
    devices = list_devices()
    result: List[BluezDevice1] = []

    for device in devices:
        # if device is connected add to result list
        if device.Connected:
            result.append(device)

    return result


def discover_and_connect(adapter_str: str):
    _LOGGER.debug("Bl discovery: scanning...")

    # loop trough list of devices
    for device in list_devices():
        paired: bool = device.Paired
        connected: bool = device.Connected
        uuids: List[str] = device.UUIDs

        # Connect to the device with the audio source profile,
        # if the device is paired and not connected.
        if paired and not connected and uuids.count(AUDIO_SRC) > 0:
            _LOGGER.debug(f"Bl discovery: connecting to {device.object_path}")

            if device.ConnectProfile(AUDIO_SRC):
                # wait for the device to be connected, 
                # so that the dbus doesn't get overloaded.
                while not device.Connected:
                    pass


class BluetoothError(Exception):
    pass
