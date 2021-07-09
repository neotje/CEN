"""
org.bluez.Adapter1 interface

https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/adapter-api.txt
"""
import dbus
import dbus.service

from cen_uiu.helpers import bus

INTERFACE = "org.bluez.Adapter1"


class BluezAdapter1(bus.Object):
    def __init__(self, conn: dbus.Bus, object_path: str):
        super().__init__(INTERFACE, conn=conn, object_path=object_path)

    @dbus.service.method(INTERFACE)
    def StartDiscovery(self):
        pass

    @dbus.service.method(INTERFACE)
    def StopDiscovery(self):
        pass

    @dbus.service.method(INTERFACE, in_signature="o")
    def RemoveDevice(self, device: dbus.ObjectPath):
        pass

    @dbus.service.method(INTERFACE, in_signature="a{sv}")
    def SetDiscoveryFilter(self, filter: dbus.Dictionary):
        pass

    @dbus.service.method(INTERFACE, out_signature="as")
    def GetDiscoveryFilters(self):
        pass
