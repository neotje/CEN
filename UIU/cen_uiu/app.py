import pathlib
from cen_uiu import gui

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'window_state', 'visible')
Config.set('graphics', 'resizable', False)


class MainScreen(Screen):
    pass


class UIUApp(App):
    def build(self):
        # load kv file
        kv_path = pathlib.Path(gui.__path__[0]) / "app.kv"
        self.load_kv(kv_path.as_posix())

        # add screens to the screen_manager
        self.screen_manager = ScreenManager()
        self.screen_manager.add_widget(MainScreen(name="main"))

        return self.screen_manager
