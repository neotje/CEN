
from cen_uiu.gui.HomeScreen import HomeScreen
from kivy.uix.screenmanager import ScreenManager


class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MainScreenManager, self).__init__()

        self.add_widget(HomeScreen())