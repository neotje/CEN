from abc import ABC


class AudioInput(ABC):
    _name: str

    @property
    def name(self) -> str:
        return self._name

    def enable(self):
        pass

    def disable(self):
        pass
