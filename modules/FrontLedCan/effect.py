from ledManager import LedManager
import math

def lerp(start, stop, amt):
    return start + (stop - start)*amt

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


        self.currentColor = (
            lerp(self.currentColor[0], target[0], dt * self.speed),
            lerp(self.currentColor[1], target[1], dt * self.speed),
            lerp(self.currentColor[2], target[2], dt * self.speed)
        )

        self.leds.fill(self.currentColor)
        