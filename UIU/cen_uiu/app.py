import pathlib
from cen_uiu import gui

from kivy.app import App
from kivy.uix.widget import Widget

from kivy.config import Config

Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '480')
Config.set('graphics', 'window_state', 'visible')
Config.set('graphics', 'resizable', False)


class Root(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UIUApp(App):
    def build(self):
        kv_path = pathlib.Path(gui.__path__[0]) / "app.kv"
        self.load_kv(kv_path.as_posix())

        return Root()
