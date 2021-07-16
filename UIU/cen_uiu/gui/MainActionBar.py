from cen_uiu.event import EventManager, ON_DARK_MODE, ON_LIGHT_MODE
from cen_uiu.helpers.gui import get_image
from kivy.config import Config

from kivy.uix.actionbar import ActionBar, ActionButton, ActionPrevious, ActionView
from kivy.utils import get_color_from_hex
from kivy.lang import Builder


Builder.load_string('''
#:import gui cen_uiu.helpers.gui
#:import event cen_uiu.event
#:import utils kivy.utils


<MainActionBar>
    background_color: utils.get_color_from_hex("#6495ED")

    ActionView:
        ActionPrevious:
            with_previous: False
            app_icon: gui.get_image("Chevrolet-logo-no-text.png")
            on_release: event.EventManager.dispatch(event.SWITCH_TO_SCREEN, {'screen': 'home'})

        ActionButton:
            text: "Nacht Modus"
            on_release: root._on_ui_mode()
''')


class MainActionBar(ActionBar):
    dark_mode: bool = False

    def __init__(self, **kwargs):
        super(MainActionBar, self).__init__()

        self.dark_mode = Config.getdefault("UIU", "dark_mode", False)

        if self.dark_mode:
            EventManager.dispatch(ON_DARK_MODE, {})
        else:
            EventManager.dispatch(ON_LIGHT_MODE, {})

    def _on_ui_mode(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            EventManager.dispatch(ON_DARK_MODE, {})
        else:
            EventManager.dispatch(ON_LIGHT_MODE, {})

        Config.set("UIU", "dark_mode", self.dark_mode)
