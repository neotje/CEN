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
