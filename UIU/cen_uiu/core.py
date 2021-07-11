import multiprocessing
import platform
from typing import Callable, Dict, List

from cen_uiu.app import UIUApp
from cen_uiu.modules.audio import BluetoothInput
from cen_uiu.modules.bluetooth import BL_ON_CONNECT_EVENT, BluetoothDiscovery
from cen_uiu.update import UpdateThread
from cen_uiu.worker import UIUCoreWorker

from kivy.logger import Logger
_LOGGER = Logger


class UIUCore:
    def __init__(self):
        _LOGGER.info("Initializing core...")
        self.bl_audio = BluetoothInput()
        self.updater = UpdateThread(self)
        self.event = Event(self)
        self.bluetooth = BluetoothDiscovery(self)

        self.app = UIUApp()

        self._worker = UIUCoreWorker(self)

        self.event.listen(BL_ON_CONNECT_EVENT, self._on_connect)

    def _on_connect(self, core, device):
        _LOGGER.info("connected to paired device.")

    def start(self):
        _LOGGER.info("starting...")

        self.bl_audio.enable()
        self.bluetooth.start()

        if platform.uname().machine == "armv7l":
            self.updater.start()

        self._worker.start()

    def stop(self):
        _LOGGER.info("stopping...")
        
        for child in multiprocessing.active_children():
            child.kill()
        
        self.bl_audio.disable()
        self.updater.stop()

    def restart(self):
        _LOGGER.info("Restarting...")
        self.bl_audio.disable()

        for child in multiprocessing.active_children():
            child.kill()

        self.updater.stop()

        exit(10)


class Event:
    def __init__(self, core: UIUCore) -> None:
        self._listeners: Dict[List[Callable]] = {}
        self._running_listeners = []

        self._core = core

    def listen(self, event: str, listener: Callable):
        self._listeners.setdefault(event, []).get(event).append(listener)

    def call(self, event: str, data: dict):
        listeners = self._listeners.get(event)

        if listeners is not None:
            for func in listeners:
                p = multiprocessing.Process(
                    group=f"event-{event}", target=func, args=(self._core, data))

                p.start()
