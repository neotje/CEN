import canio
import board
import digitalio

bus: canio.CAN = None

def setup(baudrate=250_000):
    global bus
    
    # enable can
    standby = digitalio.DigitalInOut(board.CAN_STANDBY)
    standby.switch_to_output(False)

    # enable boost converter
    boost_enable = digitalio.DigitalInOut(board.BOOST_ENABLE)
    boost_enable.switch_to_output(True)

    bus = canio.CAN(rx=board.CAN_RX, tx=board.CAN_TX, baudrate=baudrate, auto_restart=True)