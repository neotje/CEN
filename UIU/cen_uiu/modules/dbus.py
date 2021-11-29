import dbus as _dbus
from dbus.proxies import ProxyObject
import asyncio

DEFAULT_BUS = "org.bluez"

# system bus
bus = _dbus.SystemBus()


async def get_proxy_object(path: str, bus_name: str = DEFAULT_BUS) -> ProxyObject:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, bus.get_object, bus_name, path)
