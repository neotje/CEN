import subprocess
import sys

from cen_uiu.helpers.audio import AudioInput


import logging
_LOGGER = logging.getLogger(__name__)


class BluetoothInput(AudioInput):
    _bluealsa_aplay: subprocess.Popen

    def __init__(self):
        self._name = "Bluetooth"
        self._bluealsa_aplay = subprocess.Popen(["ls"], stdout=None)

    def enable(self):
        _LOGGER.debug("Enabling bluetooth input")
        self._bluealsa_aplay = subprocess.Popen(
            ["/usr/bin/bluealsa-aplay", "--profile-a2dp", "--pcm-buffer-time=250000", "00:00:00:00:00:00"], stdout=sys.stdout)

    def disable(self):
        _LOGGER.debug("Disabling bluetooth input")
        self._bluealsa_aplay.kill()
