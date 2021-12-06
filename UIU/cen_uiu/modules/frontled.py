import asyncio
import struct
from typing import List
import can
from cen_uiu.modules import can_bus
import logging

Logger = logging.getLogger(__name__)

LED_COUNT_PER_SIDE = 19


class FrontLedCan:
    _manager: can_bus.CanManager

    READY_ID = 0
    PALETTE_ID = 1
    EFFECT_ID = 2

    _current_palette = [
        (0, 0, 0),
        (0, 0, 0),
        (0, 0, 0)
    ]
    _new_palette: List[tuple] = []

    _current_effect = 0
    _new_effect: int = None


    def __init__(self, manager: can_bus.CanManager) -> None:
        self._manager = manager

    async def begin(self):
        await self._manager.listenToId(self.READY_ID, self._on_ready)

    @property
    def palette(self) -> List[tuple]:
        return self._current_palette

    @palette.setter
    def palette(self, value: List[tuple]):
        for i, color in enumerate(value):
            self._new_palette.append((i, *color))

    @property
    def effect(self) -> int:
        return self._current_effect

    @effect.setter
    def effect(self, value: int):
        self._new_effect = value

    async def _on_ready(self, e, manager: can_bus.CanManager, frame: can.Message):
        Logger.debug("frontled ready recieved.")
        if len(self._new_palette) > 0:
            Logger.info("frontled sending color palette...")
            item = self._new_palette.pop(0)
            await manager.bus.send(self.PALETTE_ID, struct.pack("<HBBB", *item))
            self._current_palette[item[0]] = item[1:]
        elif self._new_effect is not None:
            Logger.info("frontled sending effect...")
            await manager.bus.send(self.EFFECT_ID, struct.pack("<H", self._new_effect))
            self._new_effect = None
            self._current_effect = self._new_effect

