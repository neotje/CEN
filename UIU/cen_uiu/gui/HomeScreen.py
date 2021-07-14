from cen_uiu.helpers.gui import get_image
from cen_uiu.modules.bluetooth import list_connected_devices
from cen_uiu.modules.interfaces.media_api import BluezMediaPlayer1
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.graphics import Rectangle, Color

"""
HomeScreen
    Boxlayout
        StackLayout
            song_label
            album_label
            artist_label
        BoxLayout
            previous_button
            play_button
            next_button

"""


class HomeScreen(Screen):
    def __init__(self, **kw):
        super(HomeScreen, self).__init__()

        self.name = "home"
        self._player: BluezMediaPlayer1 = None

        # background
        self.canvas.before.add(Color(get_color_from_hex("#ffffff")))
        self.canvas.before.add(Rectangle(size=(800, 480)))

        player_container = BoxLayout(orientation='vertical')
        player_container = RelativeLayout()
        
        song_info_container = RelativeLayout()
        self.song_label = Label(text="song", color=(0, 0, 0))
        self.song_label.font_size = 30
        self.song_label.size_hint = (None, None)
        self.song_label.halign = 'left'
        self.song_label.pos_hint = {'center_y': .8, 'center_x': .5}

        self.album_label = Label(text="album", color=(0, 0, 0))
        self.album_label.size_hint = (None, None)
        self.album_label.halign = 'left'
        self.album_label.pos_hint = {'center_y': .7, 'center_x': .5}

        self.artist_label = Label(text="artist", color=(0, 0, 0))
        self.artist_label.size_hint = (None, None)
        self.artist_label.halign = 'left'
        self.artist_label.pos_hint = {'center_y': .6, 'center_x': .5}

        control_container = RelativeLayout()

        button_size = (80, 80)

        previous_button = Button(color=(0, 0, 0))
        previous_button.background_normal = get_image("previous.png")
        previous_button.size = button_size
        previous_button.texture_size = button_size
        previous_button.pos_hint = {'center_y': .25, 'center_x': .33}
        previous_button.size_hint = (None, None)

        play_button = Button(color=(0, 0, 0))
        play_button.background_normal = get_image("play.png")
        play_button.size = button_size
        play_button.pos_hint = {'center_y': .25, 'center_x': .5}
        play_button.size_hint = (None, None)

        self.play_button = play_button

        next_button = Button(color=(0, 0, 0))
        next_button.background_normal = get_image("next.png")
        next_button.size = button_size
        next_button.pos_hint = {'center_y': .25, 'center_x': .66}
        next_button.size_hint = (None, None)

        previous_button.bind(on_press=self._on_previous)
        play_button.bind(on_press=self._on_play_pause)
        next_button.bind(on_press=self._on_next)

        player_container.add_widget(self.song_label)
        player_container.add_widget(self.album_label)
        player_container.add_widget(self.artist_label)

        player_container.add_widget(previous_button)
        player_container.add_widget(play_button)
        player_container.add_widget(next_button)

        #player_container.add_widget(song_info_container)
        #player_container.add_widget(control_container)

        self.add_widget(player_container)

        def update(dt):
            connected = list_connected_devices()

            if len(connected) == 0:
                self.song_label.text = "No device connected."
                self.artist_label.text = ""
                self.album_label.text = ""
            else:
                player = None

                for device in connected:
                    control = device.MediaControl

                    if control is not None:
                        player = control.Player

                self._player = player

                self._on_track()
                self._on_status()

        Clock.schedule_interval(update, 0.5)

    def _on_play_pause(self, instance):
        if self._player is not None:
            if self._player.Status == "playing":
                self._player.Pause()
            else:
                self._player.Play()

    def _on_next(self, instance):
        if self._player is not None:
            self._player.Next()

    def _on_previous(self, instance):
        if self._player is not None:
            self._player.Previous()

    def _on_status(self):
        if self._player is not None:
            if self._player.Status == "playing":
                self.play_button.background_normal = get_image("play.png")
                return
        self.play_button.background_normal = get_image("pause.png")

    def _on_track(self):
        if self._player is not None:
            try:
                self.song_label.text = self._player.Track["Title"]
            except KeyError:
                self.song_label.text = "unkown"

            try:
                self.artist_label.text = self._player.Track["Artist"]
            except KeyError:
                self.artist_label.text = "unkown"

            try:
                self.album_label.text = self._player.Track["Album"]
            except KeyError:
                self.album_label.text = "unkown"
        else:
            self.song_label.text = "No bluetooth player"
            self.artist_label.text = ""
            self.album_label.text = ""
