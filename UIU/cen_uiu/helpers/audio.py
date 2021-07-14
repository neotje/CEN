from abc import ABC


class status:
    PLAYING = 0
    PAUSED = 1
    ERROR = 2


class AudioInput(ABC):
    _name: str

    @property
    def name(self) -> str:
        return self._name

    @classmethod
    def enable(self):
        pass
    
    @classmethod
    def disable(self):
        pass


class MediaSource(ABC):
    @property
    def title(self) -> str or None:
        return

    @property
    def album(self) -> str or None:
        return

    @property
    def artist(self) -> str or None:
        return

    @property
    def duration(self) -> int or None:
        return

    @property
    def position(self) -> int or None:
        return

    @property
    def status(self) -> int:
        return

    
