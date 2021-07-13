import dbus
from dbus.proxies import ProxyObject

# system bus
bus = dbus.SystemBus()


def get_proxy_object(path: str) -> ProxyObject:
    return bus.get_object("org.bluez", path)
