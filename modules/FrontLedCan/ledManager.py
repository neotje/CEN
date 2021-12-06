import neopixel

class LedManager:
    strips = []

    _count = 0
    _maxCount = 0

    def __init__(self) -> None:
        pass

    @property
    def count(self):
        return self._count

    @property
    def maxLedCount(self):
        return self._maxCount

    def addStrip(self, pin, ledCount):
        self.strips.append(neopixel.NeoPixel(pin, ledCount, brightness=1, auto_write=False, pixel_order="RGB"))
        self._count += ledCount

        if ledCount > self.maxLedCount:
            self._maxCount = ledCount

    def fill(self, color: tuple):
        for strip in self.strips:
            strip.fill(color)

    def setPixel(self, i: int, color: tuple):
        for strip in self.strips:
            if i < strip.n:
                strip[i] = color
                return
            
            i -= strip.n

    def show(self):
        for strip in self.strips:
            strip.show()