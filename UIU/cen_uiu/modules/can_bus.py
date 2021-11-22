import can
import os

from can import interface

class canBus:
    _channel: str
    _bitrate: int
    _bus: can.Bus

    def __init__(self, channel="can0", restart=0) -> None:
        self._channel = channel

    def begin(self, bitrate, restart=None):
        os.system(f'sudo ip link set {self._channel} type can bitrate {bitrate}')

        if restart is not None:
            os.system(f"sudo ip link set {self._channel} type can restart-ms {restart}")

        self.setUp(True)

        self._bus = can.Bus(self._channel, interface="socketcan")


    def setUp(self, state):
        os.system(f'sudo ifconfig {self._channel} {"up" if state else "down"}')
