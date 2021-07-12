"""
standard dbus interfaces
https://dbus.freedesktop.org/doc/dbus-specification.html#standard-interfaces
"""

import subprocess
import re
from typing import List
from cen_uiu.helpers.task import Task
import dbus
from dbus.exceptions import DBusException
from dbus.proxies import ProxyObject

from dbus_next.aio import MessageBus
import asyncio
from dbus_next.constants import BusType
from dbus_next.signature import Variant

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


async def async_get_proxy_object(path: str):
    return bus.get_object("org.bluez", path)


def get_interface_property(interface: dbus.Interface, name: str):
    try:
        properties_interface = dbus.Interface(
            interface, "org.freedesktop.DBus.Properties")

        return properties_interface.Get(interface.dbus_interface, name)
    except DBusException:
        return None


async def async_get_interface_property(interface: dbus.Interface, name: str):
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


async def async_set_interface_property(interface: dbus.Interface, name: str, value) -> bool:
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


async def async_get_adapter(name: str) -> dbus.Interface:
    """
    https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/adapter-api.txt
    """
    device_proxy_object = await async_get_proxy_object(f"/org/bluez/{name}")
    return dbus.Interface(device_proxy_object, "org.bluez.Adapter1")


def get_agent() -> dbus.Interface:
    """
    https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/agent-api.txt
    """
    device_proxy_object = get_proxy_object("/org/bluez")
    return dbus.Interface(device_proxy_object, "org.bluez.AgentManager1")


async def async_get_agent() -> dbus.Interface:
    """
    https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/agent-api.txt
    """
    device_proxy_object = await async_get_proxy_object("/org/bluez")
    return dbus.Interface(device_proxy_object, "org.bluez.AgentManager1")


def get_device(adapter: str, device: str) -> dbus.Interface:
    """
    https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/device-api.txt
    """
    device_proxy_object = get_proxy_object(
        f"/org/bluez/{adapter}/dev_{device}")
    return dbus.Interface(device_proxy_object, "org.bluez.Device1")


async def async_get_device(adapter: str, device: str) -> dbus.Interface:
    """
    https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/device-api.txt
    """
    device_proxy_object = await async_get_proxy_object(
        f"/org/bluez/{adapter}/dev_{device}")
    return dbus.Interface(device_proxy_object, "org.bluez.Device1")


def get_media_player(device: dbus.Interface) -> dbus.Interface:
    return dbus.Interface(device, "org.bluez.MediaPlayer1")


async def async_get_media_player(device: dbus.Interface) -> dbus.Interface:
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


async def async_list_devices() -> List[str]:
    proxy = await get_proxy_object("/")
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


class BluetoothDiscovery(Task):
    def __init__(self, core, adapter: str = "hci0"):
        self._core = core
        self._adapter = adapter

    async def async_run(self):
        _LOGGER.info("Bluetooth discovery: running...")

        bus = await MessageBus(bus_type=BusType.SYSTEM).connect()

        # get adapter
        intros = await bus.introspect("org.bluez", f"/org/bluez/{self._adapter}")
        proxy = bus.get_proxy_object("org.bluez", f"/org/bluez/{self._adapter}", intros)
        adapter = proxy.get_interface("org.bluez.Adapter1")
        adapter_props = proxy.get_interface("org.freedesktop.DBus.Properties")

        # make adapter discoverable and start scanning for devices
        await adapter_props.call_set("org.bluez.Adapter1", "Discoverable", Variant('b', True))

        try:
            await adapter.call_start_discovery()
        except DBusException:
            pass

        while True:
            for device in await async_list_devices():
                # get device
                intros = await bus.introspect("org.bluez", f"/org/bluez/{self._adapter}/dev_{device}")
                proxy = bus.get_proxy_object("org.bluez", f"/org/bluez/{self._adapter}/dev_{device}", intros)
                device = proxy.get_interface("org.bluez.Device1")
                device_props = proxy.get_interface("org.freedesktop.DBus.Properties")

                paired: bool = await device_props.call_get("org.bluez.Device1", "Paired")
                connected: bool = await device_props.call_get("org.bluez.Device1", "Connected")
                uuids: List[str] = await device_props.call_get("org.bluez.Device1", "UUIDs")

                # if device is paired not connected and has the audio src uuid connect to it
                if paired and not connected and uuids.count(AUDIO_SRC) > 0:
                    try:
                        await device.call_connect_profile(AUDIO_SRC)
                    except DBusException:
                        continue

                    while not await device_props.call_get("org.bluez.Device1", "Connected"):
                        pass

                    self._core.event.call(
                        BL_ON_CONNECT_EVENT, {"device": device})


class BluetoothError(Exception):
    pass
