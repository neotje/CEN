"""
https://git.kernel.org/pub/scm/bluetooth/bluez.git/tree/doc/media-api.txt
"""

from cen_uiu.helpers.bus import BusObject
from cen_uiu.modules.dbus import get_proxy_object
import dbus


class BluezMediaTransport1(BusObject):
    INTERFACE = "org.bluez.MediaTransport1"

    @property
    def Device(self) -> dbus.ObjectPath:
        return self._get_prop("Device")

    @property
    def Volume(self) -> dbus.UInt16:
        return self._get_prop("Volume")

    @Volume.setter
    def Volume(self, val: int):
        self._set_prop("Volume", dbus.UInt16(val * 1.27))


class BluezMediaPlayer1(BusObject):
    INTERFACE = "org.bluez.MediaPlayer1"

    async def Play(self):
        return await self.run_in_executor(self._interface.Play)

    async def Pause(self):
        return await self.run_in_executor(self._interface.Pause)

    async def Stop(self):
        return await self.run_in_executor(self._interface.Stop)

    async def Next(self):
        return await self.run_in_executor(self._interface.Next)

    async def Previous(self):
        return await self.run_in_executor(self._interface.Previous)

    async def FastForward(self):
        return await self.run_in_executor(self._interface.FastForward)

    async def Rewind(self):
        return await self.run_in_executor(self._interface.Rewind)

    @property
    def Status(self) -> dbus.String:
        return self._get_prop("Status")

    @property
    def Position(self) -> dbus.UInt32:
        p = self._get_prop("Position")
        
        if p is None:
            return 0

        return p

    @property
    def Track(self) -> dbus.Dictionary:
        return self._get_prop("Track")

    @property
    def Name(self) -> dbus.String:
        return self._get_prop("Name")

    @property
    def Device(self) -> dbus.ObjectPath:
        return self._get_prop("Device")


async def getBluezMediaPlayer(path):
    if path is None:
        return None

    prox = await get_proxy_object(path)
    return BluezMediaPlayer1(prox)

class BluezMediaControl1(BusObject):
    INTERFACE = "org.bluez.MediaControl1"

    @property
    def Connected(self) -> dbus.Boolean:
        return self._get_prop("Connected")

    @property
    async def Player(self) -> BluezMediaPlayer1 or None:
        path = self._get_prop("Player")

        return await getBluezMediaPlayer(path)

