import struct
import time

import board
import canio
import digitalio

import neopixel

READY_ID = 0
PALETTE_ID = 1
EFFECT_ID = 2

strips = [
    neopixel.NeoPixel(board.A3, 19, brightness=1, auto_write=False, pixel_order="RGB"),
    neopixel.NeoPixel(board.A2, 19, brightness=1, auto_write=False, pixel_order="RGB"),
    #neopixel.NeoPixel(board.A3, LED_COUNT, brightness=1, auto_write=False, pixel_order="RGB"),
    #neopixel.NeoPixel(board.A3, LED_COUNT, brightness=1, auto_write=False, pixel_order="RGB")
]

# enable can
standby = digitalio.DigitalInOut(board.CAN_STANDBY)
standby.switch_to_output(False)

# enable boost converter
boost_enable = digitalio.DigitalInOut(board.BOOST_ENABLE)
boost_enable.switch_to_output(True)    

led = digitalio.DigitalInOut(board.NEOPIXEL_POWER)
led.switch_to_output(True)
pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3)

colors = [
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0)
]
effect = 0

def fill(color: tuple):
    for strip in strips:
        strip.fill(color)

def setPixel(i, color: tuple):
    for strip in strips:
        if i < strip.n:
            strip[i] = color
            return
        
        i -= strip.n

def show():
    for strip in strips:
        strip.show()

def getLedCount():
    count = 0
    for strip in strips:
        count += strip.n
    return count

def handleMsg(msg: canio.Message):
    global colors, effect

    print(msg.id)

    if msg.id == PALETTE_ID:
        index, r, g, b = struct.unpack("<HBBB", msg.data)
        colors[index] = (r, g, b)
    elif msg.id == EFFECT_ID:
        effect = struct.unpack("<H", msg.data)[0]

can = canio.CAN(rx=board.CAN_RX, tx=board.CAN_TX, baudrate=250_000, auto_restart=True)
listener = can.listen(timeout=0)

readyMsg = canio.Message(READY_ID, b'')

while True:
    can.send(readyMsg)
    msg = listener.receive()

    if msg is not None:
        pixel.fill([255, 255, 0])
        handleMsg(msg)
        pixel.fill([0, 0, 0])

    if effect == 0:
        fill(colors[0])

    show()
    