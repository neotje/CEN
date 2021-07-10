import subprocess
import sys

from cen_uiu.helpers.audio import AudioInput

from kivy.logger import Logger
_LOGGER = Logger


class BluetoothInput(AudioInput):
    _bluealsa_aplay: subprocess.Popen

    def __init__(self):
        self._name = "Bluetooth"
        self._bluealsa_aplay = None

    def enable(self):
        _LOGGER.debug("Enabling bluetooth input")

        try:
            self._bluealsa_aplay = subprocess.Popen(
                ["/usr/bin/bluealsa-aplay", "--profile-a2dp", "--pcm-buffer-time=250000", "00:00:00:00:00:00"], stdout=sys.stdout)
        except Exception:
            pass

    def disable(self):
        _LOGGER.debug("Disabling bluetooth input")

        try:
            self._bluealsa_aplay.kill()
        except Exception:
            pass
