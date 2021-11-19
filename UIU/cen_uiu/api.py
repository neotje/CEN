import asyncio
import logging
from typing import Any
from cen_uiu.modules.ble import BLEDevice
from cen_uiu.modules.frontled import FrontLedConnection
import webview

from cen_uiu.modules.audio import BluetoothInput
from cen_uiu.modules.bluetooth import AUDIO_SRC, get_adapter, get_device, list_devices
from cen_uiu.modules import brightness, settings, system

Logger = logging.getLogger(__name__)

ADAPTER = "hci0"


class UIUapi:
    frontLedConnection: FrontLedConnection

    def __init__(self):
        self.adapter = get_adapter(ADAPTER)
        self.bl_audio = BluetoothInput()
        self.bl_device = None
        self.frontLedConnection = None

    async def quit(self):
        for window in webview.windows:
            window.destroy()

    async def toggle_fullscreen(self):
        for window in webview.windows:
            window.toggle_fullscreen()

    async def bl_devices(self):
        Logger.debug("bl_devices")

        devices = [
            d.to_object() for d in list_devices()
        ]

        return {
            "devices": devices
        }

    async def bl_pair(self, addr: str):
        Logger.debug("bl_pair")

        dev = get_device(ADAPTER, addr)

        if bool(dev.Paired):
            return {"device": dev.to_object()}

        dev.Pair()

        for i in range(30):
            await asyncio.sleep(1)

            if bool(dev.Paired):
                return {"device": dev.to_object()}

        return {"failed": True}

    async def bl_remove_device(self, addr: str):
        Logger.debug("bl_remove_device")

        dev = get_device(ADAPTER, addr)

        self.adapter.RemoveDevice(dev.object_path)

    async def bl_connect(self, addr: str):
        Logger.debug("bl_connect")

        dev = get_device(ADAPTER, addr)

        # if device is already connect just return the device object.
        if bool(dev.Connected):
            return {"device": dev.to_object()}

        # connect using to audo source profile.
        if dev.ConnectProfile(AUDIO_SRC):
            while not dev.Connected:
                pass
            return {"device": dev.to_object()}
        return {"device": None}

    async def bl_current(self):
        Logger.debug("bl_current")
        if self.bl_device is not None:
            return {"device": self.bl_device.to_object()}
        return {"device": None}

    async def bl_adapter_discoverable(self, state: bool):
        Logger.debug("bl_adapter_discoverable")
        self.adapter.Discoverable = state

    async def bl_adapter_discovery(self, state: bool):
        Logger.debug("bl_adapter_discovery")
        if state and not self.adapter.Discovering:
            self.adapter.StartDiscovery()
        elif not state and self.adapter.Discovering:
            self.adapter.StopDiscovery()

    async def bl_is_discovering(self):
        Logger.debug("bl_is_discovering")

        return {"discovering": bool(self.adapter.Discovering)}

    async def bl_enable_audio(self, addr: str):
        """
        enable bluetooth audio output by bluetooth device address.
        """
        Logger.debug("bl_enable_audio")

        if self.bl_device is not None and addr == self.bl_device.Address:
            return

        self.bl_audio.enable(addr)

        self.bl_device = get_device(ADAPTER, addr)
        self.bl_device.MediaControl.Player.Play()

    async def bl_disable_audio(self):
        Logger.debug("bl_disable_audio")
        self.bl_audio.disable()

        if self.bl_device is not None:
            self.bl_device.MediaControl.Player.Stop()
            self.bl_device = None

    async def bl_play(self):
        Logger.debug("bl_play")
        if self.bl_device is not None:
            self.bl_device.MediaControl.Player.Play()

    async def bl_pause(self):
        Logger.debug("bl_pause")
        if self.bl_device is not None:
            self.bl_device.MediaControl.Player.Pause()

    async def bl_next(self):
        Logger.debug("bl_next")
        if self.bl_device is not None:
            self.bl_device.MediaControl.Player.Next()

    async def bl_previous(self):
        Logger.debug("bl_previous")
        if self.bl_device is not None:
            self.bl_device.MediaControl.Player.Previous()

    async def bl_track(self):
        Logger.debug("bl_track")
        if self.bl_device is not None:
            return self.bl_device.MediaControl.Player.Track

    async def bl_position(self):
        Logger.debug("bl_position")
        if self.bl_device is not None:
            return self.bl_device.MediaControl.Player.Position

    async def bl_status(self):
        Logger.debug("bl_status")
        if self.bl_device is not None:
            player = self.bl_device.MediaControl.Player

            return {
                "status": player.Status,
                "position": player.Position,
                "track": player.Track
            }

        return {
            "status": "paused",
            "position": 0
        }

    async def settings_getAll(self):
        return settings.getAll()

    async def settings_set(self, key: str, val: Any):
        settings.set(key, val)
        return {
            "value": settings.get(key)
        }

    async def settings_get(self, key: str):
        return {
            "value": settings.get(key)
        }

    async def brightness_get(self):
        Logger.debug("brightness_get")
        return {
            "value": brightness.getBrightness()
        }

    async def brightness_set(self, level: int):
        Logger.debug("brightness_set")
        brightness.setBrightness(round(level))
        return {}

    async def system_reboot(self):
        system.reboot()
        return {}

    async def system_shutdown(self):
        system.shutdown()
        return {}

    async def frontLed_available(self):
        if self.frontLedConnection is None:
            return {"available": False}

        if self.frontLedConnection._device.isConnected():
            return {"available": True, "device": self.frontLedConnection.device.to_object()}
        else:
            return {"available": False}

    async def frontLed_loadDevice(self, addr: str):
        if addr is None: return {}
        
        bleDevice = BLEDevice(addr)

        self.frontLedConnection = FrontLedConnection(bleDevice)

        return {}

    async def frontLed_fill(self, side: str, color: str):
        if self.frontLedConnection is None:
            return {"available": False}

        if side == "left":
            self.frontLedConnection.fillLeft(color)
        elif side == "right":
            self.frontLedConnection.fillRight(color)
        elif side == "all":
            self.frontLedConnection.fill(color)

        return {"available": True, "device": self.frontLedConnection.device.to_object()}

    async def frontLed_set(self, side: str, index: int, color: str):
        if self.frontLedConnection is None:
            return {"available": False}

        if side == "left":
            self.frontLedConnection.setLeft(index, color)
        elif side == "right":
            self.frontLedConnection.setRight(index, color)
        elif side == "all":
            self.frontLedConnection.set(index, color)

        return {"available": True}
