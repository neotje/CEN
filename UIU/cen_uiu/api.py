import asyncio
import logging
from typing import Any
from cen_uiu.helpers.api_base import ApiBase
from cen_uiu.modules.can_bus import AsyncCanBus, CanBus, CanManager
from cen_uiu.modules.frontled import FrontLedCan
from cen_uiu.modules.interfaces.adapter_api import BluezAdapter1
from dbus.exceptions import DBusException
import webview

from cen_uiu.modules.audio import BluetoothInput
from cen_uiu.modules.bluetooth import AUDIO_SRC, get_adapter, get_device, list_devices
from cen_uiu.modules import brightness, settings, system

Logger = logging.getLogger(__name__)

ADAPTER = "hci0"


class UIUapi(ApiBase):
    frontLedCan: FrontLedCan
    canManager: CanManager
    adapter: BluezAdapter1

    def __init__(self):
        self.bl_audio = BluetoothInput()
        self.bl_device = None

    async def _setup(self):
        self.adapter = await get_adapter(ADAPTER)
        self.canManager = CanManager()
        await self.canManager.openBus(250_000)

        self.frontLedCan = FrontLedCan(self.canManager)
        await self.frontLedCan.begin()

    async def bl_devices(self):
        Logger.debug("bl_devices")

        devices = [
            await d.to_object() for d in await list_devices()
        ]

        return {
            "devices": devices
        }

    async def bl_pair(self, addr: str):
        Logger.debug("bl_pair")

        dev = await get_device(ADAPTER, addr)

        if bool(await dev.Paired):
            return {"device": await dev.to_object()}

        await dev.Pair()

        for i in range(30):
            await asyncio.sleep(1)

            if bool(await dev.Paired):
                return {"device": await dev.to_object()}

        return {"failed": True}

    async def bl_remove_device(self, addr: str):
        Logger.debug("bl_remove_device")

        dev = await get_device(ADAPTER, addr)

        await self.adapter.RemoveDevice(dev.object_path)

    async def bl_connect(self, addr: str):
        Logger.debug("bl_connect")

        dev = await get_device(ADAPTER, addr)

        # if device is already connect just return the device object.
        if bool(await dev.Connected):
            return {"device": await dev.to_object()}

        # connect using to audo source profile.
        try:
            await dev.ConnectProfile(AUDIO_SRC)
            while not await dev.Connected:
                pass
            return {"device": await dev.to_object()}
        except DBusException:
            pass
        return {"device": None}

    async def bl_connectUUID(self, addr: str, uuid: str):
        Logger.debug("bl_connectUUID")

        dev = await get_device(ADAPTER, addr)

        # if device is already connect just return the device object.
        """ if bool(await dev.Connected):
            return {"device": await dev.to_object()} """

        # connect using to audo source profile.
        await dev.ConnectProfile(AUDIO_SRC)
        return {"device": await dev.to_object()}

    async def bl_disconnectUUID(self, addr: str, uuid: str):
        Logger.debug("bl_disconnectUUID")

        dev = await get_device(ADAPTER, addr)

        await dev.DisconnectProfile(uuid)
        return {}

    async def bl_current(self):
        Logger.debug("bl_current")
        if self.bl_device is not None:
            return {"device": await self.bl_device.to_object()}
        return {"device": None}

    async def bl_adapter_discoverable(self, state: bool):
        Logger.debug("bl_adapter_discoverable")
        await self.adapter.setDiscoverable(state)

    async def bl_adapter_discovery(self, state: bool):
        Logger.debug("bl_adapter_discovery")
        discovering = await self.adapter.Discovering

        if state and not discovering:
            await self.adapter.StartDiscovery()
        elif not state and discovering:
            await self.adapter.StopDiscovery()

    async def bl_is_discovering(self):
        Logger.debug("bl_is_discovering")

        return {"discovering": bool(await self.adapter.Discovering)}

    async def bl_enable_audio(self, addr: str):
        """
        enable bluetooth audio output by bluetooth device address.
        """
        Logger.debug("bl_enable_audio")

        if self.bl_device is not None and addr == await self.bl_device.Address:
            return

        self.bl_audio.enable(addr)

        self.bl_device = await get_device(ADAPTER, addr)
        control = await self.bl_device.MediaControl
        player = await control.Player
        if player is not None:
            await player.Play()

    async def bl_disable_audio(self):
        Logger.debug("bl_disable_audio")
        self.bl_audio.disable()

        if self.bl_device is not None:
            control = await self.bl_device.MediaControl
            player = await control.Player

            if player is None:
                return

            await player.Stop()
            await self.bl_device.DisconnectProfile(AUDIO_SRC)
            self.bl_device = None

    async def bl_play(self):
        Logger.debug("bl_play")
        if self.bl_device is not None:
            control = await self.bl_device.MediaControl
            player = await control.Player
            if player is not None:
                await player.Play()

    async def bl_pause(self):
        Logger.debug("bl_pause")
        if self.bl_device is not None:
            control = await self.bl_device.MediaControl
            player = await control.Player
            await player.Pause()

    async def bl_next(self):
        Logger.debug("bl_next")
        if self.bl_device is not None:
            control = await self.bl_device.MediaControl
            player = await control.Player
            await player.Next()

    async def bl_previous(self):
        Logger.debug("bl_previous")
        if self.bl_device is not None:
            control = await self.bl_device.MediaControl
            player = await control.Player
            await player.Previous()

    async def bl_track(self):
        Logger.debug("bl_track")
        if self.bl_device is not None:
            control = await self.bl_device.MediaControl
            player = await control.Player
            return await player.Track

    async def bl_position(self):
        Logger.debug("bl_position")
        if self.bl_device is not None:
            control = await self.bl_device.MediaControl
            player = await control.Player
            return await player.Position

    async def bl_status(self):
        Logger.debug("bl_status")
        if self.bl_device is not None:
            control = await self.bl_device.MediaControl
            player = await control.Player

            return {
                "status": await player.Status,
                "position": await player.Position,
                "track": await player.Track
            }

        return {
            "status": "paused",
            "position": 0
        }

    async def settings_getAll(self):
        return await settings.getAll()

    async def settings_set(self, key: str, val: Any):
        await settings.set(key, val)
        return {
            "value": await settings.get(key)
        }

    async def settings_get(self, key: str):
        return {
            "value": await settings.get(key)
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

    async def system_softReboot(self):
        system.softReboot()
        return {}

    async def frontLed_fill(self, side: str, color: tuple):
        self.frontLedCan.palette = [color]
        self.frontLedCan.effect = 0
        return {"status": "online"}
