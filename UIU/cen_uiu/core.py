import os
import sys
from cen_uiu.app import UIUApp
from cen_uiu.modules.audio import BluetoothInput
from cen_uiu.update import UpdateThread
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
        _LOGGER.info("starting...")
        self.bl_audio.enable()
        self.updater.start()
        self._worker.start()

    def stop(self):
        _LOGGER.info("stopping...")
        self.bl_audio.disable()
        self._worker.stop()
        self.updater.stop()

    def restart(self):
        _LOGGER.info("Restarting...")
        self.bl_audio.disable()
        self._worker.stop()
        self._worker.join()
        self.updater.stop()

        exit(10)
