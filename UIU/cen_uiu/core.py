from functools import partial
import screeninfo

# cen_uiu
from cen_uiu.app import UIUApp
from cen_uiu.modules.audio import BluetoothInput
from cen_uiu.modules.bluetooth import discover_and_connect, get_adapter
from cen_uiu.update import check_and_update

# kivy
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.logger import Logger
_LOGGER = Logger


class UIUCore:
    def __init__(self):
        _LOGGER.info("Initializing core...")

        self.bl_audio = BluetoothInput()

        UIUApp.configure()
        self.app = UIUApp(self)

        self.exit_code: int = 0

    def start(self):
        _LOGGER.info("core: starting...")

        self.bl_audio.enable()

        adapter = get_adapter("hci0")
        adapter.Discoverable = True
        # adapter.StartDiscovery()

        Clock.schedule_once(partial(discover_and_connect, self, "hci0"), 5)
        Clock.schedule_interval(partial(check_and_update, self), 60)

        monitor = screeninfo.get_monitors()[0]
        Window.size = (800, 480)
        if monitor.width == 800 and monitor.height == 480:
            Window.fullscreen = True

        self.app.run()

    def stop(self):
        _LOGGER.info("stopping...")
        self.exit_code = 0

        self.bl_audio.disable()
        self.app.stop()

    def restart(self, *args):
        _LOGGER.info("Restarting...")
        self.exit_code = 10

        self.bl_audio.disable()
        self.app.stop() 
