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
        self._set_prop("Volume", val)


class BluezMediaPlayer1(BusObject):
    INTERFACE = "org.bluez.MediaPlayer1"

    def Play(self):
        return self._interface.Play()

    def Pause(self):
        return self._interface.Pause()

    def Stop(self):
        return self._interface.Stop()

    def Next(self):
        return self._interface.Next()

    def Previous(self):
        return self._interface.Previous()

    def FastForward(self):
        return self._interface.FastForward()

    def Rewind(self):
        return self._interface.Rewind()

    @property
    def Status(self) -> dbus.String:
        return self._get_prop("Status")

    @property
    def Position(self) -> dbus.UInt32:
        return self._get_prop("Position")

    @property
    def Track(self) -> dbus.Dictionary:
        return self._get_prop("Track")

    @property
    def Name(self) -> dbus.String:
        return self._get_prop("Name")

    @property
    def Device(self) -> dbus.ObjectPath:
        return self._get_prop("Device")


class BluezMediaControl1(BusObject):
    INTERFACE = "org.bluez.MediaControl1"

    @property
    def Connected(self) -> dbus.Boolean:
        return self._get_prop("Connected")

    @property
    def Player(self) -> BluezMediaPlayer1 or None:
        path = self._get_prop("Player")

        if path is not None:
            prox = get_proxy_object(path)
            return BluezMediaPlayer1(dbus.Interface(prox, BluezMediaPlayer1.INTERFACE))

        return None

