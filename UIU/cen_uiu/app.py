from kivy.app import App
from kivy.uix.widget import Widget


class Root(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class UIUApp(App):
    def build(self):
        self.load_kv
        return Root()
