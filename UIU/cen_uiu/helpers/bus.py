import dbus
from dbus.proxies import ProxyObject

from kivy.logger import Logger
_LOGGER = Logger

class BusObject:
    INTERFACE: str

    def __init__(self, interface: ProxyObject or dbus.Interface) -> None:
        self._interface: dbus.Interface = dbus.Interface(interface, self.INTERFACE)
        self._props: dbus.Interface = dbus.Interface(interface, "org.freedesktop.DBus.Properties")

    def _get_prop(self, name: str):
        try:
            return self._props.Get(self._interface.dbus_interface, name)
        except dbus.DBusException:
            return None

    def _set_prop(self, name: str, val):
        try:
            return self._props.Set(self._interface.dbus_interface, name, val)
        except dbus.DBusException as e:
            _LOGGER.error(f"BusObject: something went wrong with setting the property {name} to {val}")
            _LOGGER.error(e)
            pass

    @property
    def object_path(self) -> str:
        return self._interface.object_path
