"""
RootLayout:
    MainScreensManager
        HomeScreen
    MainActionBar
"""

from cen_uiu.event import EventManager, ON_STOP
from cen_uiu.gui.MainActionBar import MainActionBar
from cen_uiu.gui.MainScreenManager import MainScreenManager

# kivy
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.modules import inspector
from kivy.core.window import Window


class RootLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(RootLayout, self).__init__()

        self.orientation = 'vertical'

        self.add_widget(MainScreenManager())
        self.add_widget(MainActionBar())


class UIUApp(App):
    def __init__(self, core, **kwargs):
        super().__init__(**kwargs)

        self.core = core

    @classmethod
    def configure(self):
        Config.set('graphics', 'height', 480)
        Config.set('graphics', 'width', 800)
        Config.set('graphics', 'window_state', 'visible')
        Config.set('graphics', 'resizable', False)
        Config.set('graphics', 'multisamples', 1)

        Config.adddefaultsection("UIU")

    def build(self):
        # load kv file
        """ kv_path = pathlib.Path(gui.__path__[0]) / "app.kv"
        self.load_kv(kv_path.as_posix()) """

        layout = RootLayout()
        inspector.create_inspector(Window, layout)
        return layout

    def switch_to(self, screen_name: str):
        for s in self.screen_manager.screens:
            if s.name == screen_name:
                self.screen_manager.switch_to(s)

    def on_stop(self):
        EventManager.dispatch(ON_STOP, {})
        Config.write()
        self.core.stop()
