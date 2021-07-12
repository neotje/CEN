"""
org.bluez.Device1 interface

https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/device-api.txt
"""
from typing import List

from cen_uiu.helpers import bus
import dbus


class BluezDevice1(bus.BusObject):
    def Connect(self):
        return self._interface.Connect()

    def Disconnect(self):
        return self._interface.Disconnect()

    def ConnectProfile(self, uuid: dbus.String):
        return self._interface.ConnectProfile(uuid)

    def DisconnectProfile(self, uuid: dbus.String):
        return self._interface.DisconnectProfile(uuid)

    def Pair(self):
        return self._interface.Pair()

    def CancelPairing(self):
        return self._interface.CancelPairing()

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
    