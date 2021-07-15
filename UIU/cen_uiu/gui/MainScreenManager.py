
from cen_uiu.event import EventManager, SWITCH_TO_SCREEN
from cen_uiu.gui.HomeScreen import HomeScreen
from kivy.uix.screenmanager import ScreenManager


class MainScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super(MainScreenManager, self).__init__()

        self.add_widget(HomeScreen())

        EventManager.listen(
            SWITCH_TO_SCREEN, lambda data: self._switch_to_event(data))

    def _switch_to_event(self, data: dict):
        name = data.get("screen")

        for screen in self.screens:
            if screen.name == name:
                self.switch_to(screen)
