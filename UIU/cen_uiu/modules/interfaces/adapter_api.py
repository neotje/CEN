"""
org.bluez.Adapter1 interface

https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/adapter-api.txt
"""
import asyncio
from typing import List
from cen_uiu.helpers import bus
import dbus
from dbus.exceptions import DBusException


class BluezAdapter1(bus.BusObject):
    INTERFACE = "org.bluez.Adapter1"

    async def StartDiscovery(self):
        try:
            return await self.run_in_executor(self._interface.StartDiscovery)
        except DBusException:
            pass

    async def StopDiscovery(self):
        try:
            return await self.run_in_executor(self._interface.StopDiscovery)
        except DBusException:
            pass

    async def RemoveDevice(self, device: dbus.ObjectPath):
        return await self.run_in_executor(self._interface.RemoveDevice, device)

    async def SetDiscoveryFilter(self, filter: dbus.Dictionary):
        return  await self.run_in_executor(self._interface.StartDiscovery, filter)

    async def GetDiscoveryFilters(self) -> List[str]:
        return await self.run_in_executor(self._interface.GetDiscoveryFilters)

    @property
    def Address(self) -> dbus.String:
        return self._get_prop("Address")

    @property
    def Name(self) -> dbus.String:
        return self._get_prop("Name")

    @property
    def Class(self) -> dbus.Int32:
        return self._get_prop("Class")

    @property
    def Powered(self) -> dbus.Boolean:
        return self._get_prop("Powered")

    @Powered.setter
    def Powered(self, val: dbus.Boolean):
        self._set_prop("Powered", val)

    @property
    def Discoverable(self) -> dbus.Boolean:
        return self._get_prop("Discoverable")

    @Discoverable.setter
    def Discoverable(self, val: dbus.Boolean):
        self._set_prop("Discoverable", val)

    @property
    def Pairable(self) -> dbus.Boolean:
        return self._get_prop("Pairable")

    @Pairable.setter
    def Pairable(self, val: dbus.Boolean):
        self._set_prop("Pairable", val)

    @property
    def Discovering(self) -> dbus.Boolean:
        return self._get_prop("Discovering")

    @Discovering.setter
    def Discovering(self, val: dbus.Boolean):
        self._set_prop("Discovering", val)
