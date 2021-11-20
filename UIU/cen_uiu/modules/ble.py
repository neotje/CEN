"""
DEPRECATED!
"""

from typing import Any, List
import gattlib

import logging

from webview.event import Event
Logger = logging.getLogger(__name__)


def read(device: str, uuid: str):
    requester = gattlib.GATTRequester(device, False)

    Logger.debug(f"Connecting to ble device: {device}")
    requester.connect(True)
    Logger.debug(f"OK: {device}")

    return requester.read_by_uuid(uuid)


class BLERequester(gattlib.GATTRequester):
    notification = Event()

    def on_notification(self, handle, data):
        self.notification.set(handle, data)


class BLEDevice:
    _name: str
    _address: str
    _requester: BLERequester

    def __init__(self, address, name="") -> None:
        self._address = address
        self._name = name
        self._requester = BLERequester(address, False)

    def _uuidToHandle(self, uuid: str) -> int:
        self.connect()
        characteristics = self._requester.discover_characteristics()

        for char in characteristics:
            if char['uuid'] == uuid:
                return char['value_handle']

    @property
    def address(self) -> str:
        return self._address

    @property
    def name(self) -> str:
        return self._name

    @property
    def services(self) -> List:
        #self.connect()
        primary_services = self._requester.discover_primary()

        return [prim['uuid'] for prim in primary_services]

    @property
    def characteristics(self) -> List[str]:
        self.connect()

        characteristics = self._requester.discover_characteristics()

        return [char['uuid'] for char in characteristics]

    @property
    def isConnected(self) -> bool:
        return self._requester.is_connected()

    def to_object(self) -> dict:
        return {
            "Name": self.name,
            "Address": self.address,
            "Connected": self.isConnected
        }

    def hasService(self, uuid: str) -> bool:
        services = self.services
        return uuid in services

    def connect(self, wait=True):
        if not self._requester.is_connected():
            self._requester.connect(wait)

    def disconnect(self):
        self._requester.disconnect()

    def read(self, uuid: str) -> bytes:
        self.connect()

        data = self._requester.read_by_uuid(uuid)

        return data[0]

    def write(self, uuid: str, value: Any):
        handle = self._uuidToHandle(uuid)

        value = str(value).encode("utf-8")

        self._requester.write_by_handle_async(handle, value, gattlib.GATTResponse())

    def addOnNotification(self, listener):
        self._requester.notification += listener

    def __repr__(self) -> str:
        return f"address: {self.address} name: {self.name}"


def discover(adapter="hci0", timeout=2) -> dict:
    discovery = gattlib.DiscoveryService(adapter)
    devices = discovery.discover(timeout)

    deviceObjects = []

    for address, name in list(devices.items()):
        deviceObjects.append(BLEDevice(address, name))


    return deviceObjects
