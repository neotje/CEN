from typing import Callable, List
from kivy.clock import Clock
from kivy.logger import Logger
_LOGGER = Logger

# system events
ON_STOP = "on_stop"

# ui events
ON_DARK_MODE = "on_dark_mode"
ON_LIGHT_MODE = "on_light_mode"

ON_SCREEN_SWITCH = "on_main_screen_switch"
SWITCH_TO_SCREEN = "main_switch_to_screen"


class EventBaseManager:
    def __init__(self) -> None:
        self.listeners: dict[str, List[Callable[[int, dict], None]]] = {}

    def listen(self, evt: str, func: Callable[[dict], None]):
        self.listeners.setdefault(evt, []).append(func)

    def dispatch(self, evt: str, data: dict):
        _LOGGER.debug(f"Event manager: dispatching event {evt}")
        functions = self.listeners.get(evt)

        if functions is None:
            return

        for f in self.listeners[evt]:
            Clock.schedule_once(lambda dt: f(data), -1)


EventManager = EventBaseManager()
