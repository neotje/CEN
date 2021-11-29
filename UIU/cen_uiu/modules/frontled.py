import asyncio
import struct
from cen_uiu.modules import can_bus

LED_COUNT_PER_SIDE = 19


class FrontLedCan:
    _bus: can_bus.AsyncCanBus
    _count: int

    LED_COUNT_ID = 2
    FILL_ID = 3
    SET_ID = 4
    SHOW_ID = 5

    def __init__(self, bus: can_bus.AsyncCanBus) -> None:
        self._bus = bus

    async def begin(self):
        await self.requestLedCount()

    async def requestLedCount(self) -> int:
        msg = await self._bus.send(self.LED_COUNT_ID, b'', wait=True)
        self._count, = struct.unpack("<H", msg.data)
        return self._count

    @property
    def ledCount(self):
        return self._count

    async def fill(self, color: tuple):
        await self._bus.send(self.FILL_ID, struct.pack("<BBB", *color))

    async def show(self):
        await self._bus.send(self.SHOW_ID, b'', wait=True)