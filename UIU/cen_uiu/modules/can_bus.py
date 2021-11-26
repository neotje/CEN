import can
import os
import asyncio
import logging
Logger = logging.getLogger(__name__)


class CanBus:
    _channel: str
    _bitrate: int
    _bus: can.Bus
    _notfier: can.Notifier

    def __init__(self, channel="can0", restart=0) -> None:
        self._channel = channel

    def begin(self, bitrate, restart=None):
        self.setUp(False)

        os.system(
            f'sudo ip link set {self._channel} type can bitrate {bitrate}')

        if restart is not None:
            os.system(
                f"sudo ip link set {self._channel} type can restart-ms {restart}")

        self.setUp(True)

        self._bus = can.Bus(self._channel, interface="socketcan")
        self._notfier = can.Notifier(self._bus, [])

    def setUp(self, state):
        os.system(f'sudo ifconfig {self._channel} {"up" if state else "down"}')

    def recv(self, timeout=1) -> can.Message:
        return self._bus.recv(timeout)

    def send(self, id: int, data: bytes, retry=True, wait=False, extended_id=False):
        """send can frame

        Example:
        ```bus.send(3, struct.pack("<BBB", 0, 0, 0))```

        Args:
            id (int): [description]
            data (bytes): [description]
            retry (bool, optional): [description]. Defaults to True.
            wait (bool, optional): [description]. Defaults to False.
        """
        msg = can.Message(arbitration_id=id, data=data, extended_id=extended_id)
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


class AsyncCanBus(CanBus):
    async def send(self, id: int, data: bytes, retry=True, wait=False, extended_id=False):
        loop = asyncio.get_running_loop()

        return await asyncio.wait_for(
            loop.run_in_executor(None, super().send, id, data, retry, wait, extended_id),
            1
        )

    async def getAsyncReader(self) -> can.AsyncBufferedReader:
        reader = can.AsyncBufferedReader()
        self._notfier.add_listener(reader)
        return reader

    async def begin(self, bitrate, restart=None):
        loop = asyncio.get_running_loop()

        await loop.run_in_executor(None, super().begin, bitrate, restart)

        self._notfier = can.Notifier(self._bus, [], loop=loop)

    async def recv(self, timeout=1) -> can.Message:
        loop = asyncio.get_running_loop()

        try:
            return await asyncio.wait_for(
                loop.run_in_executor(None, self._bus.recv, timeout),
                timeout
            )
        except asyncio.TimeoutError:
            Logger.debug("Recieve timout reached!")
            return None
    
