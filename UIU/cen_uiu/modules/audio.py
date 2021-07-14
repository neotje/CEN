import subprocess
import sys

from cen_uiu.helpers.audio import AudioInput, MediaSource
from cen_uiu.modules.bluetooth import list_connected_devices
from cen_uiu.modules.interfaces.media_api import BluezMediaPlayer1

from kivy.logger import Logger
_LOGGER = Logger


class NotConnected(Exception):
    pass


class BluetoothInput(AudioInput):
    _bluealsa_aplay: subprocess.Popen

    def __init__(self):
        self._name = "Bluetooth"
        self._bluealsa_aplay = None

    def enable(self, addr: str = "00:00:00:00:00:00"):
        _LOGGER.debug("Enabling bluetooth input")

        if self._bluealsa_aplay is not None:
            self.disable()

        try:
            # start aplay process
            self._bluealsa_aplay = subprocess.Popen(
                ["/usr/bin/bluealsa-aplay", "--profile-a2dp", "--pcm-buffer-time=500000", addr], stdout=sys.stdout)
        except Exception:
            pass

    def disable(self):
        _LOGGER.debug("Disabling bluetooth input")

        try:
            # stop aplay process and wait for it to die
            self._bluealsa_aplay.kill()
            self._bluealsa_aplay.wait()
            self._bluealsa_aplay = None
        except Exception:
            pass
