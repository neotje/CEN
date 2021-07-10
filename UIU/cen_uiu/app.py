from kivy.app import App
from kivy.uix.widget import Widget

from kivy.config import Config

Config.set('graphics', 'width', '200')
Config.set('graphics', 'height', '200')
Config.set('graphics', 'window_state', 'hidden')


class Root(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UIUApp(App):
    def build(self):
        self.load_kv
        return Root()
