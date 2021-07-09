import dbus
import dbus.service


class Object(dbus.service.Object):
    _interface: str

    def __init__(self, interface: str, conn=None, object_path=None, bus_name=None):
        super().__init__(conn=conn, object_path=object_path, bus_name=bus_name)

        self._interface = interface

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ss', out_signature='v')
    def Get(self, interface: dbus.String, name: dbus.String):
        pass

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='s', out_signature='a{sv}')
    def GetAll(self, interface: dbus.String):
        pass

    @dbus.service.method(dbus.PROPERTIES_IFACE, in_signature='ssv')
    def Set(self, interface: dbus.String, name: dbus.String, value):
        pass
