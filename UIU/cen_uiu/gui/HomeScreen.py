from cen_uiu.modules.bluetooth import list_connected_devices
from cen_uiu.modules.interfaces.media_api import BluezMediaPlayer1
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.utils import get_color_from_hex
from kivy.graphics import Rectangle, Color


class HomeScreen(Screen):
    def __init__(self, **kw):
        super(HomeScreen, self).__init__()

        self.name = "home"

        self.canvas.before.add(Color(get_color_from_hex("#ffffff")))
        self.canvas.before.add(Rectangle(size=(800, 480)))

        layout = BoxLayout()
        layout.orientation = 'vertical'
        
        song_label = Label(text="song", color=(0, 0, 0))
        artist_label = Label(text="artist", color=(0, 0, 0))

        layout.add_widget(song_label)
        layout.add_widget(artist_label)
        self.add_widget(layout)

        def update(dt):
            connected = list_connected_devices()

            if len(connected) == 0:
                song_label.text = "No device connected."
                artist_label.text = ""
            else:
                active: BluezMediaPlayer1

                for device in connected:
                    control = device.MediaControl

                    if control is not None:
                        player = control.Player
                        if player is not None:
                            active = player

                if active is not None:
                    song_label.text = active.Track["Title"]
                    artist_label.text = active.Track["Artist"]
                else:
                    song_label.text = "No bluetooth player"
                    artist_label.text = ""

        Clock.schedule_interval(update, 1)
