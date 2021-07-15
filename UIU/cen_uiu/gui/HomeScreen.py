from cen_uiu.event import EventManager, ON_DARK_MODE, ON_LIGHT_MODE
from cen_uiu.helpers.gui import get_image
from cen_uiu.modules.bluetooth import list_connected_devices
from cen_uiu.modules.interfaces.media_api import BluezMediaPlayer1
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, ObjectProperty
from kivy.animation import Animation

from kivy.logger import Logger
_LOGGER = Logger

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

Builder.load_string('''
#:import gui cen_uiu.helpers.gui

<HomeScreen>:
    id: home
    progressbar: bar
    play_button: play_btn

    canvas.before:
        Color:
            rgb: self.background_color
        Rectangle:
            size: self.size

    RelativeLayout:
        Label:
            text: root.song
            color: root.text_color
            pos_hint: {'center_y': .8, 'center_x': .5}
            font_size: 30
        Label:
            text: root.artist
            color: root.text_color
            pos_hint: {'center_y': .7, 'center_x': .5}
            font_size: 20
        Label:
            text: root.album
            color: root.text_color
            pos_hint: {'center_y': .6, 'center_x': .5}

        ProgressBar:
            id: bar
            max: 100
            value: 100
            pos_hint: {'center_y': .5, 'center_x': .5}
            size_hint_x: .7

        Button:
            background_normal: gui.get_image("previous.png")
            size: 70, 70
            size_hint: None, None
            pos_hint: {'center_y': .25, 'center_x': .33}
            on_release: root._on_previous()
        Button:
            id: play_btn
            background_normal: gui.get_image("play.png")
            size: 70, 70
            size_hint: None, None
            pos_hint: {'center_y': .25, 'center_x': .5}
            on_release: root._on_play_pause()
        Button:
            background_normal: gui.get_image("next.png")
            size: 70, 70
            size_hint: None, None
            pos_hint: {'center_y': .25, 'center_x': .66}
            on_release: root._on_next()
''')


class HomeScreen(Screen):

    song = StringProperty("song")
    album = StringProperty("album")
    artist = StringProperty("artist")

    background_color = ListProperty([1, 1, 1])
    text_color = ListProperty([0, 0, 0])

    progressbar = ObjectProperty()
    play_button = ObjectProperty()

    animation: Animation = None

    def __init__(self, **kw):
        super(HomeScreen, self).__init__()

        self.name = "home"
        self._player: BluezMediaPlayer1 = None

        EventManager.listen(ON_DARK_MODE, self.dark_mode)
        EventManager.listen(ON_LIGHT_MODE, self.light_mode)

        def update(dt):
            connected = list_connected_devices()

            if len(connected) == 0:
                self.song = "No device connected."
                self.artist = ""
                self.album = ""
            else:
                player = None

                for device in connected:
                    control = device.MediaControl

                    if control is not None:
                        player = control.Player

                self._player = player

                self._on_track()
                self._on_status()

        Clock.schedule_interval(update, 0.2)

    def _on_play_pause(self):
        if self._player is not None:
            if self._player.Status == "playing":
                _LOGGER.debug("Media: pause")
                self._player.Pause()
            else:
                _LOGGER.debug("Media: play")
                self._player.Play()

    def _on_next(self):
        if self._player is not None:
            _LOGGER.debug("Media: next song")
            self._player.Next()

    def _on_previous(self):
        if self._player is not None:
            _LOGGER.debug("Media: previous song")
            self._player.Previous()

    def _on_status(self):
        if self._player is not None:
            try:
                duration = self._player.Track["Duration"]
                pos = self._player.Position
                self.progressbar.max = int(duration)
                self.progressbar.value = int(pos)

            except KeyError or TypeError:
                pass
            if self._player.Status == "playing":
                self.play_button.background_normal = get_image("pause.png")
                return
        self.play_button.background_normal = get_image("play.png")

    def _on_track(self):
        if self._player is not None:
            try:
                self.song = self._player.Track["Title"]
            except KeyError or TypeError:
                self.song = "unkown"

            try:
                self.artist = self._player.Track["Artist"]
            except KeyError or TypeError:
                self.artist = "unkown"

            try:
                self.album = self._player.Track["Album"]
            except KeyError or TypeError:
                self.album = "unkown"
        else:
            self.song = "No bluetooth player"
            self.artist = ""
            self.album = ""

    def dark_mode(self, d: dict):
        if self.animation is not None:
            self.animation.stop(self)
        self.animation = Animation(background_color=(0, 0, 0), text_color=(1, 1, 1))
        self.animation.start(self)

    def light_mode(self, d: dict):
        if self.animation is not None:
            self.animation.stop(self)
        self.animation = Animation(background_color=(1, 1, 1), text_color=(0, 0, 0))
        self.animation.start(self)
