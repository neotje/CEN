"""
org.bluez.Device1 interface

https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/device-api.txt
"""
from typing import List

from cen_uiu.helpers import bus
from cen_uiu.modules.dbus import get_proxy_object
from cen_uiu.modules.interfaces.media_api import BluezMediaControl1, BluezMediaTransport1
import dbus
from dbus.exceptions import DBusException


class BluezDevice1(bus.BusObject):
    INTERFACE = "org.bluez.Device1"

    def Connect(self):
        return self._interface.Connect()

    def Disconnect(self):
        return self._interface.Disconnect()

    def ConnectProfile(self, uuid: dbus.String):
        try:
            self._interface.ConnectProfile(uuid)
            return True
        except DBusException:
            return False

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

    @property
    def MediaControl(self) -> BluezMediaControl1 or None:
        try:
            interface = dbus.Interface(
                self._interface, BluezMediaControl1.INTERFACE)
            return BluezMediaControl1(interface)
        except DBusException:
            return None

    @property
    def MediaTransport(self) -> BluezMediaTransport1 or None:
        try:
            interface = dbus.Interface(get_proxy_object(
                self._interface.object_path + "/fd0"), BluezMediaTransport1.INTERFACE)
            return BluezMediaTransport1(interface)
        except DBusException:
            return None
