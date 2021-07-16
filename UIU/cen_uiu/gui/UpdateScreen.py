from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string('''
#:import utils kivy.utils

<UpdateScreen>:
    canvas.before:
        Color:
            rgb: utils.get_color_from_hex("#03adfc")
        Rectangle:
            size: self.size

    BoxLayout:
        Label:
            font_size: 30
            text: "Updaten..."
''')


class UpdateScreen(Screen):
    def __init__(self, **kw):
        super(UpdateScreen, self).__init__(**kw)

        self.name = "update"
