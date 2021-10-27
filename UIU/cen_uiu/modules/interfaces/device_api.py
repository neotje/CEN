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
    def MediaTransport(self) -> BluezMediaTransport1 or None:
        # FIXME: detection for fd1, fd2, etc

        proxy = get_proxy_object("/")
        manager = dbus.Interface(proxy, "org.freedesktop.DBus.ObjectManager")
        objects = manager.GetManagedObjects()

        addr = self.Address.replace(":", "_")
        reg_dev = re.compile(f"\/org\/bluez\/hci\d*\/dev_{addr}\/fd(\d*)")
        try:
            for key, value in objects.items():
                m = reg_dev.match(key)

                if m is not None:

                    interface = dbus.Interface(get_proxy_object(
                        key), BluezMediaTransport1.INTERFACE)
                    return BluezMediaTransport1(interface)
            return None
        except DBusException:
            return None
