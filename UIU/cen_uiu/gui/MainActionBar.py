from cen_uiu.event import EventManager, ON_DARK_MODE, ON_LIGHT_MODE
from cen_uiu.helpers.gui import get_image

from kivy.uix.actionbar import ActionBar, ActionButton, ActionPrevious, ActionView
from kivy.utils import get_color_from_hex


class MainActionPrevious(ActionPrevious):
    def __init__(self, **kwargs):
        super(MainActionPrevious, self).__init__()

        self.with_previous = True
        self.app_icon = get_image("Chevrolet-logo-no-text.png")


class MainActionView(ActionView):
    def __init__(self, **kwargs):
        super(MainActionView, self).__init__()

        self.action_previous = MainActionPrevious()

        self.dark_mode = False

        self.dark_mode_btn = ActionButton()
        self.dark_mode_btn.text = "Nacht modus"
        self.dark_mode_btn.bind(on_press=lambda t: self._on_ui_mode())

        self.add_widget(ActionButton(text="home"))
        self.add_widget(self.dark_mode_btn)

    def _on_ui_mode(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            EventManager.dispatch(ON_DARK_MODE, {})
        else:
            EventManager.dispatch(ON_LIGHT_MODE, {})


class MainActionBar(ActionBar):
    def __init__(self, **kwargs):
        super(MainActionBar, self).__init__()

        self.background_color = get_color_from_hex("#6495ED")
        self.opacity = 1

        self.add_widget(MainActionView())