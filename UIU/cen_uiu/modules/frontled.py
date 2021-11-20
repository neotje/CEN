from cen_uiu.helpers.exceptions import InvalidBLEDeviceException
from cen_uiu.modules.interfaces.device_api import BluezDevice1
from cen_uiu.modules.interfaces.gattCharacteristic_api import GattCharacteristic1

LED_STRIP_SERVICE = "dff41a39-471b-4ca1-a837-c76895946d78"
LEFT_STRIP_CHARACTERISTIC = "2abd4adf-6a44-4e5e-8c84-aee36271e72c"
RIGHT_STRIP_CHARACTERISTIC = "bfccc1f0-8824-438c-8a03-c68fe0db4ce5"
FILL_STRIPS_CHARACTERISTIC = "ef89321d-9616-4cff-8f27-c10002e950a4"
LED_COUNT_PER_SIDE = 19


class FrontLedConnection:
    _device: BluezDevice1

    _fillChar: GattCharacteristic1
    _rightChar: GattCharacteristic1
    _leftChar: GattCharacteristic1

    def __init__(self, bleDevice: BluezDevice1) -> None:
        self._device = bleDevice
        self._device.Connect()

        self.check_device()

        self._fillChar = bleDevice.GATTCharacteristic(FILL_STRIPS_CHARACTERISTIC)
        self._rightChar = bleDevice.GATTCharacteristic(RIGHT_STRIP_CHARACTERISTIC)
        self._leftChar = bleDevice.GATTCharacteristic(LEFT_STRIP_CHARACTERISTIC)

    @property
    def device(self) -> BluezDevice1:
        return self._device

    def check_device(self):
        if not LED_STRIP_SERVICE in self._device.UUIDs:
            raise InvalidBLEDeviceException(
                f"{self._device} does not have the LED strip service UUID")

    def setLeft(self, index, color: str):
        if index < 0 or index >= LED_COUNT_PER_SIDE:
            return

        index = str(index)

        if len(index) < 2:
            index = f"0{index}"

        color = color.replace("#", "0x")
        self._leftChar.WriteValue(f"{index}{color}")

    def setRight(self, index, color):
        if index < 0 or index >= LED_COUNT_PER_SIDE:
            return

        index = str(index)

        if len(index) < 2:
            index = f"0{index}"

        color = color.replace("#", "0x")
        self._rightChar.WriteValue(f"{index}{color}")

    def set(self, index, color: str):
        if index < LED_COUNT_PER_SIDE:
            self.setLeft(LED_COUNT_PER_SIDE - index - 1, color)
        else:
            self.setRight(index - LED_COUNT_PER_SIDE, color)

    def fillLeft(self, color: str):
        for i in range(LED_COUNT_PER_SIDE):
            self.setLeft(i, color)

    def fillRight(self, color: str):
        for i in range(LED_COUNT_PER_SIDE):
            self.setRight(i, color)

    def fill(self, color: str):
        color = color.replace("#", "0x")
        self._fillChar.WriteValue(f"{color}")