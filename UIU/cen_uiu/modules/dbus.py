import dbus as _dbus
from dbus.proxies import ProxyObject

DEFAULT_BUS = "org.bluez"

# system bus
bus = _dbus.SystemBus()


def get_proxy_object(path: str, bus_name: str = DEFAULT_BUS) -> ProxyObject:
    return bus.get_object(bus_name, path)
