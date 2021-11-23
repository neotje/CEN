import can
import os
import asyncio

from can import interface

class CanBus:
    _channel: str
    _bitrate: int
    _bus: can.Bus
    _notfier: can.Notifier
    _async_reader: can.AsyncBufferedReader

    def __init__(self, channel="can0", restart=0) -> None:
        self._channel = channel

    def begin(self, bitrate, restart=None):
        self.setUp(False)

        os.system(f'sudo ip link set {self._channel} type can bitrate {bitrate}')

        if restart is not None:
            os.system(f"sudo ip link set {self._channel} type can restart-ms {restart}")

        self.setUp(True)

        self._bus = can.Bus(self._channel, interface="socketcan")

    async def begin_async(self, bitrate, restart=None):
        self.begin(bitrate, restart)

        self._notfier = can.Notifier(self._bus, [], loop=asyncio.get_event_loop())
        self._async_reader = self.getAsyncReader()

    def setUp(self, state):
        os.system(f'sudo ifconfig {self._channel} {"up" if state else "down"}')

    def getAsyncReader(self) -> can.AsyncBufferedReader:
        reader = can.AsyncBufferedReader()
        self._notfier.add_listener(reader)
        return reader

    def recv(self, timeout=1) -> can.Message:
        return self._bus.recv(timeout)

    async def send_async(self, id: int, data: bytes, retry=True, wait=False):
        msg = can.Message(arbitration_id=id, data=data)

        while True:
            try:
                self._bus.send(msg, 10)
                retry = False
            except can.CanError:
                pass

            if not retry:
                break

        if wait:
            while True:
                msg = await self._async_reader.get_message()

                if msg.arbitration_id == id:
                    return msg


    def send(self, id: int, data: bytes, retry=True, wait=False):
        """send can frame

        Example:
        ```bus.send(3, struct.pack("<BBB", 0, 0, 0))```

        Args:
            id (int): [description]
            data (bytes): [description]
            retry (bool, optional): [description]. Defaults to True.
            wait (bool, optional): [description]. Defaults to False.
        """
        msg = can.Message(arbitration_id=id, data=data)        
        while True:
            try:
                self._bus.send(msg, 10)
                retry = False
            except can.CanError:
                pass

            if not retry:
                break
        
        if wait:
            for msg in self._bus:
                if msg.arbitration_id == id:
                    return msg

                
