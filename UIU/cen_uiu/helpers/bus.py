import asyncio
import dbus
from dbus.proxies import ProxyObject

import logging
Logger = logging.getLogger(__name__)
_LOGGER = Logger

"""
bus object
used to interface with a dbus proxy or interface object.
used to create subclasses (act as a baseclass).
"""
class BusObject:
    INTERFACE: str

    def __init__(self, interface: ProxyObject or dbus.Interface) -> None:
        self._interface: dbus.Interface = dbus.Interface(interface, self.INTERFACE)
        self._props: dbus.Interface = dbus.Interface(interface, "org.freedesktop.DBus.Properties")

    # cal this function to get a property of a dbus object.
    async def _get_prop(self, name: str):
        try:
            return await self.run_in_executor(self._props.Get, self._interface.dbus_interface, name)
        except dbus.DBusException:
            return None

    # call this function to set a property of a dbus object.
    async def _set_prop(self, name: str, val):
        try:
            return await self.run_in_executor(self._props.Set, self._interface.dbus_interface, name, val)
        except dbus.DBusException as e:
            _LOGGER.error(f"BusObject: something went wrong with setting the property {name} to {val}")
            _LOGGER.error(e)
            pass
    
    # object path property.
    @property
    def object_path(self) -> str:
        return self._interface.object_path

    async def run_in_executor(self, func, *args):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, func, *args)
