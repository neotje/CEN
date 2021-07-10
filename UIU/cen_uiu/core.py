import os
import sys
from cen_uiu.app import UIUApp
from cen_uiu.modules.audio import BluetoothInput
from cen_uiu.modules.update import UpdateThread
from cen_uiu.worker import UIUCoreWorker

from kivy.logger import Logger
_LOGGER = Logger


class UIUCore:
    def __init__(self):
        _LOGGER.info("Initializing core...")
        self.bl_audio = BluetoothInput()
        self.updater = UpdateThread(self)
        self.app = UIUApp()
        self._worker = UIUCoreWorker(self)

    def start(self):
        self.bl_audio.enable()
        self.updater.start()
        self._worker.start()

    def stop(self):
        self.bl_audio.disable()
        self._worker.stop()
        self.updater.stop()

    def restart(self):
        self._worker.stop()
        self._worker.join()
        os.execv(sys.argv[0], sys.argv)
