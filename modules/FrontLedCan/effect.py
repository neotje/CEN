from ledManager import LedManager
import math

def lerp(start, stop, amt):
    return (stop - start)*amt + start

def lerpColor(c1, c2, amt):
    return (
        lerp(c1[0], c2[0], amt),
        lerp(c1[1], c2[1], amt),
        lerp(c1[2], c2[2], amt)
    )

class Effect:
    _id: int
    leds: LedManager

    def __init__(self, id, leds) -> None:
        self._id = id
        self.leds = leds

    @property
    def id(self):
        return self._id
    
    def run(self, dt: float, pallete: list):
        pass


class FillEffect(Effect):
    currentColor = (0, 0, 0)
    speed = 10

    def run(self, dt: float, pallete: list):
        target = pallete[0]

        self.currentColor = lerpColor(self.currentColor, target, 0.05)

        self.leds.fill(self.currentColor)
        