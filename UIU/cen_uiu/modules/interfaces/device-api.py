"""
org.bluez.Device1 interface

https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/device-api.txt
"""
import dbus
import dbus.service

from cen_uiu.helpers import bus


class BluezDevice1(bus.Object):
    def __init__(self, conn, object_path):
        super().__init__(conn=conn, object_path=object_path)

    @dbus.service.method("org.bluez.Device1")
    def Connect(self):
        pass

    @dbus.service.method("org.bluez.Device1")
    def Disconnect(self):
        pass

    @dbus.service.method("org.bluez.Device1", in_signature="s")
    def ConnectProfile(self, uuid: dbus.String):
        pass

    @dbus.service.method("org.bluez.Device1", in_signature="s")
    def DisconnectProfile(self, uuid: dbus.String):
        pass

    @dbus.service.method("org.bluez.Device1")
    def Pair(self):
        pass

    @dbus.service.method("org.bluez.Device1")
    def CancelPairing(self):
        pass
