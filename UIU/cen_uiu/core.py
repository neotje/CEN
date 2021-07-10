from cen_uiu.app import UIUApp
from cen_uiu.modules.audio import BluetoothInput
from cen_uiu.modules.update import UpdateThread
from cen_uiu.worker import UIUCoreWorker

from kivy.logger import Logger
_LOGGER = Logger


class UIUCore:
    bl_audio: BluetoothInput
    updater: UpdateThread
    app: UIUApp

    _process: UIUCoreWorker

    def __init__(self) -> None:
        _LOGGER.info("Initializing core...")
        self.bl_audio = BluetoothInput()
        self.updater = UpdateThread(self)
        self.app = UIUApp()
        self._process = UIUCoreWorker(self)

        self.updater.start()

    def start(self):
        _LOGGER.info("Starting core worker...")
        self._process.start()

    def stop(self):
        self._process.stop()

    def restart(self):
        self._process.stop()
        self._process.join()
        self._process.start()
