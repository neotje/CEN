from functools import partial

# cen_uiu
from cen_uiu.app import UIUApp
from cen_uiu.modules.audio import BluetoothInput
from cen_uiu.modules.bluetooth import discover_and_connect
from cen_uiu.update import check_and_update

# kivy
from kivy.clock import Clock
from kivy.logger import Logger
_LOGGER = Logger


class UIUCore:
    def __init__(self):
        _LOGGER.info("Initializing core...")

        self.bl_audio = BluetoothInput()
        self.app = UIUApp(self)

        self.exit_code: int = 0

    def start(self):
        _LOGGER.info("core: starting...")

        self.bl_audio.enable()

        Clock.schedule_interval(partial(discover_and_connect, self, "hci0"), 3)
        Clock.schedule_interval(partial(check_and_update, self), 60)

        self.app.run()

    def stop(self):
        _LOGGER.info("stopping...")
        self.exit_code = 0

        self.bl_audio.disable()
        self.app.stop()

    def restart(self):
        _LOGGER.info("Restarting...")
        self.exit_code = 10

        self.bl_audio.disable()
        self.app.stop()
