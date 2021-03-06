"""
this file is responsible for connecting and discovering bluetooth devices.

standard dbus interfaces
https://dbus.freedesktop.org/doc/dbus-specification.html#standard-interfaces
"""
import asyncio
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


def formatAddress(a: str) -> str:
    return a.replace(':', '_')


async def get_adapter(name: str) -> BluezAdapter1:
    """
    https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/adapter-api.txt
    """
    device_proxy_object = await get_proxy_object(f"/org/bluez/{name}")
    return BluezAdapter1(device_proxy_object)


async def get_device(adapter: str, device: str) -> BluezDevice1:
    """
    https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/device-api.txt
    """
    device = formatAddress(device)
    device_proxy_object = await get_proxy_object(
        f"/org/bluez/{adapter}/dev_{device}")
    return BluezDevice1(device_proxy_object)


async def list_devices() -> List[BluezDevice1]:
    loop = asyncio.get_running_loop()
    proxy = await get_proxy_object("/")
    manager = dbus.Interface(proxy, "org.freedesktop.DBus.ObjectManager")

    # TODO: ObjectManager interface
    objects = await loop.run_in_executor(None, manager.GetManagedObjects)

    reg_dev = re.compile("\/org\/bluez\/hci\d*\/dev\_(.*)")
    # e.g., match a string like this:
    # /org/bluez/hci0/dev_58_C9_35_2F_A1_EF

    devices: List[BluezDevice1] = []

    for key, value in objects.items():
        m = reg_dev.match(key)

        if m is not None:
            dev_str = m.group(1)

            devices.append(await get_device("hci0", dev_str))

    return devices


async def list_connected_devices() -> List[BluezDevice1]:
    devices = await list_devices()
    result: List[BluezDevice1] = []

    for device in devices:
        # if device is connected add to result list
        if device.Connected:
            result.append(device)

    return result


async def discover_and_connect(adapter_str: str):
    _LOGGER.debug("Bl discovery: scanning...")

    # loop trough list of devices
    for device in await list_devices():
        paired: bool = await device.Paired
        connected: bool = await device.Connected
        uuids: List[str] = await device.UUIDs

        # Connect to the device with the audio source profile,
        # if the device is paired and not connected.
        if paired and not connected and uuids.count(AUDIO_SRC) > 0:
            _LOGGER.debug(f"Bl discovery: connecting to {device.object_path}")

            try:
                await device.ConnectProfile(AUDIO_SRC)
                # wait for the device to be connected,
                # so that the dbus doesn't get overloaded.
                while not await device.Connected:
                    pass
            except DBusException:
                pass


class BluetoothError(Exception):
    pass
