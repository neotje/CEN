"""
org.bluez.GattCharacteristic1 interface

https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/gatt-api.txt
"""

from typing import List
from cen_uiu.helpers import bus
from dbus.exceptions import DBusException
import dbus

class GattCharacteristic1(bus.BusObject):
    INTERFACE = "org.bluez.GattCharacteristic1"

    def ReadValue(self, options: dbus.Dictionary):
        return self._interface.ReadValue(options)

    def WriteValue(self, value: dbus.ByteArray, options: dbus.Dictionary):
        self._interface.WriteValue(value, options)

    @property
    def UUID(self) -> dbus.String:
        return self._get_prop("UUID")

    @property
    def Value(self) -> dbus.ByteArray:
        return self._get_prop("Value")

    @property
    def Flags(self) -> dbus.Array:
        return self._get_prop("Flags")