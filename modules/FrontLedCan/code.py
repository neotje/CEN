import struct
import board
import canio
import digitalio
from effect import Effect, FillEffect
from ledManager import LedManager
import neopixel
import canHelper
import time

READY_ID = 0
PALETTE_ID = 1
EFFECT_ID = 2

manager = LedManager()
manager.addStrip(board.A3, 19)
manager.addStrip(board.A2, 19)


led = digitalio.DigitalInOut(board.NEOPIXEL_POWER)
led.switch_to_output(True)
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3)

colors = [
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0)
]

effects = [
    FillEffect(0, manager)
]
currentEffect: Effect = effects[0]


def getEffect(id: int):
    for e in effects:
        if e.id == id:
            return e


def handleMsg(msg: canio.Message):
    global colors, currentEffect

    print(msg.id)

    if msg.id == PALETTE_ID:
        index, r, g, b = struct.unpack("<HBBB", msg.data)
        colors[index] = (r, g, b)
    elif msg.id == EFFECT_ID:
        id = struct.unpack("<H", msg.data)[0]
        currentEffect = getEffect(id)


readyMsg = canio.Message(READY_ID, b'')

canHelper.setup()
listener = canHelper.bus.listen(timeout=0)

while True:
    start = time.monotonic_ns()

    canHelper.bus.send(readyMsg)
    msg = listener.receive()

    if msg is not None:
        pixel.fill([255, 255, 0])
        handleMsg(msg)
        pixel.fill([0, 0, 0])

    if currentEffect is not None:
        dt = (time.monotonic_ns() - start)/1_000_000_000
        currentEffect.run(dt, colors)

    manager.show()
