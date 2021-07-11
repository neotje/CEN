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
        self.event = Event(self)
        self.app = UIUApp()

        self.exit_code = 0

        self._processes: List[multiprocessing.Process] = [
            UpdateThread(self),
            BluetoothDiscovery(self),
            UIUCoreWorker(self)
        ]

        self.event.listen(BL_ON_CONNECT_EVENT, self._on_connect)

    def _on_connect(self, core, device):
        _LOGGER.info("connected to paired device.")

    def _kill_all(self):
        for p in self._processes:
            try:
                p.kill()
            except AttributeError:
                pass
                

    def start(self):
        _LOGGER.info("starting...")

        self.bl_audio.enable()
        
        for p in self._processes:
            p.start()

    def stop(self):
        _LOGGER.info("stopping...")
        self.exit_code = 0

        self.bl_audio.disable()
        self._kill_all()

    def restart(self):
        _LOGGER.info("Restarting...")
        self.exit_code = 10

        self.bl_audio.disable()
        self._kill_all()


class Event:
    def __init__(self, core: UIUCore) -> None:
        self._listeners: Dict[List[Callable]] = {}
        self._running_listeners = []

        self._core = core

    def listen(self, event: str, listener: Callable):
        self._listeners.setdefault(event, []).append(listener)

    def call(self, event: str, data: dict):
        listeners = self._listeners.get(event)

        if listeners is not None:
            for func in listeners:
                p = multiprocessing.Process(
                    name=f"event-{event}", target=func, args=(self._core, data))

                p.start()
