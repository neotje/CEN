import pathlib
from screeninfo import get_monitors

# kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config

# cen_uiu
from cen_uiu import gui
from cen_uiu.gui.bluetooth_screen import BluetoothScreen
from cen_uiu.gui.update_screen import UpdateScreen

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')

if get_monitors[0].width == 800 and get_monitors[0].height == 480:
    Config.set('graphics', 'window_state', 'fullscreen')
else:
    Config.set('graphics', 'window_state', 'visible')

Config.set('graphics', 'resizable', False)


class MainScreen(Screen):
    pass


class UIUApp(App):
    def __init__(self, core, **kwargs):
        super().__init__(**kwargs)

        self.core = core

    def build(self):
        # load kv file
        kv_path = pathlib.Path(gui.__path__[0]) / "app.kv"
        self.load_kv(kv_path.as_posix())

        # add screens to the screen_manager
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(MainScreen(name="main"))
        self.screen_manager.add_widget(BluetoothScreen(name="bluetooth"))
        self.screen_manager.add_widget(UpdateScreen(name="update"))

        self.screen_manager.switch_to(self.screen_manager.screens[0])

        return self.screen_manager

    def switch_to(self, screen_name: str):
        for s in self.screen_manager.screens:
            if s.name == screen_name:
                self.screen_manager.switch_to(s)
