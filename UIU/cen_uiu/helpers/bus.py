import dbus


class BusObject:
    def __init__(self, interface: dbus.Interface) -> None:
        self._interface: dbus.Interface = interface
        self._props: dbus.Interface = dbus.Interface(interface, "org.freedesktop.DBus.Properties")

    def _get_prop(self, name: str):
        try:
            return self._props.Get(self._interface.dbus_interface, name)
        except dbus.DBusException:
            return None

    def _set_prop(self, name: str, val):
        try:
            return self._props.Set(self._interface.dbus_interface, name, val)
        except dbus.DBusException:
            pass

    @property
    def object_path(self) -> str:
        return self._interface.object_path
