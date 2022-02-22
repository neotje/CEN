from __future__ import annotations
import asyncio
from typing import List
import serial_asyncio
import struct
import logging

from cen_uiu.modules import settings
from cen_uiu.helpers.event import Event

Logger = logging.getLogger(__name__)


CONFIG_PORT = "serialPort"
CONFIG_BAUDRATE = "serialBaud"

CONTENT_SIZE = 4
START_BYTE = 0x1


def byteToStr(byte: int):
    binaryByte = bin(byte).replace("0b", "")

    for _ in range(8 - len(binaryByte)):
        binaryByte = "0" + binaryByte

    return binaryByte


def checksum(data: bytes) -> int:
    total = 0

    for b in data:
        total += b

    return total % 127


class Frame:
    _address: int
    _content: bytes
    _checksum: int

    def __init__(self, address: int = 0) -> None:
        self._address = address
        self._content = bytes([0x0 for i in range(CONTENT_SIZE)])
        self._checksum = checksum(self._content)

    @property
    def address(self) -> int:
        return self._address

    @address.setter
    def address(self, newAddress: int):
        if newAddress < 0 or newAddress > 255:
            raise OverflowError

        self._address = newAddress

    @property
    def content(self) -> bytes:
        return self._content

    @content.setter
    def content(self, newContent: bytes):
        if len(newContent) > CONTENT_SIZE:
            raise OverflowError

        if len(newContent) < CONTENT_SIZE:
            for i in range(CONTENT_SIZE - len(newContent)):
                newContent += bytes(0x0)

        self._content = newContent
        self._checksum = checksum(newContent)

    @property
    def checksum(self) -> bytes:
        return self._checksum

    def get_int(self) -> int:
        return struct.unpack("<h", self.content[0:2])[0]

    def get_unsigned_int(self) -> int:
        return struct.unpack("<H", self.content[0:2])[0]

    def get_long(self) -> int:
        return struct.unpack("<l", self.content)[0]

    def get_unsigned_long(self) -> int:
        return struct.unpack("<L", self.content)[0]

    def get_float(self) -> float:
        return struct.unpack("<f", self.content)[0]

    def get_string(self) -> str:
        return self.content.decode()

    def get_bin(self) -> str:
        result = ""

        for i, byte in enumerate(self.content):
            binaryByte = byteToStr(byte)

            if i > 0:
                binaryByte += "."

            result = binaryByte + result

        return result

    def set_int(self, num: int):
        self.content = struct.pack("<h", num)

    def set_unsigned_int(self, num: int):
        self.content = struct.pack("<H", num)

    def set_long(self, num: int):
        self.content = struct.pack("<l", num)

    def set_unsigned_long(self, num: int):
        self.content = struct.pack("<L", num)

    def set_float(self, num: float):
        self.content = struct.pack("<f", num)

    def verify(self) -> bool:
        return checksum(self.content) == self.checksum

    def to_bytes(self) -> bytes:
        return struct.pack(f"<BB{CONTENT_SIZE}sB", START_BYTE, self.address, self.content, self.checksum)

    @staticmethod
    def from_tuple(data: tuple) -> Frame:
        frame = Frame()

        frame._address = data[0]
        frame._content = data[1]
        frame._checksum = data[2]

        return frame

    @staticmethod
    def from_bytes(data: bytes) -> Frame:
        data = struct.unpack(f"<B{CONTENT_SIZE}sB", data)
        return Frame.from_tuple(data)

    def __repr__(self) -> str:
        return f"Frame(address={self.address}, content={self.content}, checksum={self.checksum})"


class SerialProtocol:
    _reader: asyncio.StreamReader
    _writer: asyncio.StreamWriter
    _memory: dict[int, Frame] = {}
    _onFrame: Event = Event("onFrame")

    _connected: bool = False

    @property
    def memory(self) -> List[Frame]:
        return self._memory

    @property
    def onFrame(self) -> Event:
        return self._onFrame

    @property
    def connected(self) -> bool:
        return self._connected

    async def begin(self, port: str, baudrate: int):
        try:
            self._reader, self._writer = await serial_asyncio.open_serial_connection(url=port, baudrate=baudrate)
            self._connected = True

            await self._loop()
        except serial_asyncio.serial.SerialException as e:
            Logger.error(e)
            self._connected = False
            pass

    async def send(self, frame: Frame):
        Logger.debug("Sending: " + str(frame))
        self._writer.write(frame.to_bytes())

    async def _loop(self):
        while True:
            incoming_byte: bytes = await self._reader.read(1)

            if incoming_byte[0] == START_BYTE:
                try:
                    frame_data: bytes = await asyncio.wait_for(self._reader.readexactly(6), 0.2)
                    frame = Frame.from_bytes(frame_data)

                    if frame.verify():
                        self._memory[frame.address] = frame
                        await self._onFrame.dispatch(frame, self)
                        Logger.debug("Recieved: " + str(frame))
                    else:
                        Logger.warn("Invalid frame!")
                except asyncio.TimeoutError:
                    Logger.warn("Timeout reached!")
