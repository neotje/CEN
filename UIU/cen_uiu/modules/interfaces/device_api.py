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

    async def to_object(self) -> dict:
        return {
            "Address": await self.Address,
            "Name": await self.Name,
            "Icon": await self.Icon,
            "Class": await self.Class,
            "Paired": bool(await self.Paired),
            "UUIDs": await self.UUIDs,
            "Connected": bool(await self.Connected)
        }

    async def Connect(self):
        return await self.run_in_executor(self._interface.Connect)

    async def Disconnect(self):
        return await self.run_in_executor(self._interface.Disconnect)

    async def ConnectProfile(self, uuid: dbus.String):
        await self.run_in_executor(self._interface.ConnectProfile, uuid)

    async def DisconnectProfile(self, uuid: dbus.String):
        return await self.run_in_executor(self._interface.DisconnectProfile, uuid)

    async def Pair(self):
        return await self.run_in_executor(self._interface.Pair)

    async def CancelPairing(self):
        return await self.run_in_executor(self._interface.CancelPairing)

    @property
    async def Address(self) -> dbus.String:
        return await self._get_prop("Address")

    @property
    async def Name(self) -> dbus.String:
        return await self._get_prop("Name")

    @property
    def Icon(self) -> dbus.String:
        return self._get_prop("Icon")

    @property
    async def Class(self) -> dbus.Int32:
        return await self._get_prop("Class")

    @property
    async def UUIDs(self) -> List[str]:
        return await self._get_prop("UUIDs")

    @property
    async def Paired(self) -> dbus.Boolean:
        return await self._get_prop("Paired")

    @property
    async def Connected(self) -> dbus.Boolean:
        return await self._get_prop("Connected")

    @property
    async def ServicesResolved(self) -> dbus.Boolean:
        return await self._get_prop("ServicesResolved")

    @property
    async def MediaControl(self) -> BluezMediaControl1:
        try:
            interface = dbus.Interface(
                self._interface, BluezMediaControl1.INTERFACE)
            return BluezMediaControl1(interface)
        except DBusException:
            return None

    @property
    async def MediaTransport(self) -> BluezMediaTransport1:
        # FIXME: detection for fd1, fd2, etc

        proxy = await get_proxy_object("/")
        manager = dbus.Interface(proxy, "org.freedesktop.DBus.ObjectManager")
        objects = self.run_in_executor(manager.GetManagedObjects)

        addr = (await self.Address).replace(":", "_")
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
        addr = (await self.Address).replace(":", "_")
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
