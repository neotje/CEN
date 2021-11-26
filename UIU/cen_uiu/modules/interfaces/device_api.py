"""
org.bluez.Device1 interface

https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/device-api.txt
"""
import asyncio
from typing import List

from cen_uiu.helpers import bus
from cen_uiu.modules.dbus import get_proxy_object
from cen_uiu.modules.interfaces.gattCharacteristic_api import GattCharacteristic1
from cen_uiu.modules.interfaces.media_api import BluezMediaControl1, BluezMediaTransport1
import dbus
from dbus.exceptions import DBusException

import re


class BluezDevice1(bus.BusObject):
    INTERFACE = "org.bluez.Device1"

    def to_object(self) -> dict:
        return {
            "Address": self.Address,
            "Name": self.Name,
            "Icon": self.Icon,
            "Class": self.Class,
            "Paired": bool(self.Paired),
            "UUIDs": self.UUIDs,
            "Connected": bool(self.Connected)
        }

    async def Connect(self):
        return await self.run_in_executor(self._interface.Connect)

    async def Disconnect(self):
        return await self.run_in_executor(self._interface.Disconnect)

    async def ConnectProfile(self, uuid: dbus.String):
        try:
            await self.run_in_executor(self._interface.ConnectProfile, uuid)
            return True
        except DBusException:
            return False

    async def DisconnectProfile(self, uuid: dbus.String):
        return await self.run_in_executor(self._interface.DisconnectProfile, uuid)

    async def Pair(self):
        return await self.run_in_executor(self._interface.Pair)

    async def CancelPairing(self):
        return await self.run_in_executor(self._interface.CancelPairing)

    @property
    def Address(self) -> dbus.String:
        return self._get_prop("Address")

    @property
    def Name(self) -> dbus.String:
        return self._get_prop("Name")

    @property
    def Icon(self) -> dbus.String:
        return self._get_prop("Icon")

    @property
    def Class(self) -> dbus.Int32:
        return self._get_prop("Class")

    @property
    def UUIDs(self) -> List[str]:
        return self._get_prop("UUIDs")

    @property
    def Paired(self) -> dbus.Boolean:
        return self._get_prop("Paired")

    @property
    def Connected(self) -> dbus.Boolean:
        return self._get_prop("Connected")

    @property
    def ServicesResolved(self) -> dbus.Boolean:
        return self._get_prop("ServicesResolved")

    @property
    def MediaControl(self) -> BluezMediaControl1 or None:
        try:
            interface = dbus.Interface(
                self._interface, BluezMediaControl1.INTERFACE)
            return BluezMediaControl1(interface)
        except DBusException:
            return None

    @property
    async def MediaTransport(self) -> BluezMediaTransport1 or None:
        # FIXME: detection for fd1, fd2, etc

        proxy = await get_proxy_object("/")
        manager = dbus.Interface(proxy, "org.freedesktop.DBus.ObjectManager")
        objects = self.run_in_executor(manager.GetManagedObjects)

        addr = self.Address.replace(":", "_")
        reg_dev = re.compile(f"\/org\/bluez\/hci\d*\/dev_{addr}\/fd(\d*)")
        try:
            for key, value in objects.items():
                m = reg_dev.match(key)

                if m is not None:

                    interface = dbus.Interface(
                        await get_proxy_object(key),
                        BluezMediaTransport1.INTERFACE
                    )
                    return BluezMediaTransport1(interface)
            return None
        except DBusException:
            return None

    async def GATTCharacteristic(self, uuid) -> GattCharacteristic1 or None:
        proxy = await get_proxy_object("/")
        manager = dbus.Interface(proxy, "org.freedesktop.DBus.ObjectManager")
        objects = self.run_in_executor(manager.GetManagedObjects)
        addr = self.Address.replace(":", "_")
        reg_dev = re.compile(
            f"\/org\/bluez\/hci\d*\/dev_{addr}\/service(\d*)\/char(\d*)")

        try:
            for key, value in objects.items():
                m = reg_dev.match(key)

                if m is not None:
                    interface = dbus.Interface(await get_proxy_object(key), GattCharacteristic1.INTERFACE)
                    char = GattCharacteristic1(interface)

                    if char.UUID == uuid:
                        return char
        except DBusException:
            pass
