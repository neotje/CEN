import struct
import time

import board
import canio
import digitalio

import neopixel

SYSTEM_ON_ID = 0
LED_COUNT_ID = 2
FILL_ID = 3
SET_ID = 4
SHOW_ID = 5

LED_COUNT = 38

pixels = neopixel.NeoPixel(board.A1, LED_COUNT, brightness=1, auto_write=False, pixel_order="RGB")

strips = [
    pixels
]

# enable can
standby = digitalio.DigitalInOut(board.CAN_STANDBY)
standby.switch_to_output(False)

# enable boost converter
boost_enable = digitalio.DigitalInOut(board.BOOST_ENABLE)
boost_enable.switch_to_output(True)    

can = canio.CAN(rx=board.CAN_RX, tx=board.CAN_TX, baudrate=1_000_000, auto_restart=True)
listener = can.listen()

def fill(color):
    for strip in strips:
        strip.fill(color)

def setPixel(i, color):
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

showAck = canio.Message(SHOW_ID, b'')
countMsg = canio.Message(LED_COUNT_ID, struct.pack("<H", getLedCount()))

while True:
    msg = listener.receive()

    if msg is None:
        continue

    if msg.id == SYSTEM_ON_ID:
        rpi_enable = struct.unpack("<?", msg.data)
        print(rpi_enable)
    if msg.id == LED_COUNT_ID:
        can.send(countMsg)
    elif msg.id == FILL_ID:
        color = struct.unpack("<BBB", msg.data)
        fill(color)
    elif msg.id == SET_ID:
        index, r, g, b = struct.unpack("<HBBB", msg.data)
        setPixel(index, (r, g, b))
    elif msg.id == SHOW_ID:
        show()
        can.send(showAck)