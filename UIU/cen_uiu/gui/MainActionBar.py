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

        self.add_widget(ActionButton(text="home"))
        self.add_widget(ActionButton(text="bluetooth"))


class MainActionBar(ActionBar):
    def __init__(self, **kwargs):
        super(MainActionBar, self).__init__()

        self.background_color = get_color_from_hex("#6495ED")
        self.opacity = 1

        self.add_widget(MainActionView())