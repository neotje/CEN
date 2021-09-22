import subprocess
import sys

from cen_uiu.helpers.audio import AudioInput

import logging
Logger = logging.getLogger(__name__)
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

        arguments = [
            "/usr/bin/bluealsa-aplay",
            "--profile-a2dp",
            "--pcm-buffer-time=500000",
            addr
        ]

        try:
            # start aplay process
            self._bluealsa_aplay = subprocess.Popen(arguments, stdout=sys.stdout)
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
