import sys
import logging
import asyncio
import tracemalloc
import can

from cen_uiu.modules.can_bus import CanManager
from cen_uiu.modules.frontled import FrontLedArduino
from cen_uiu.modules.serial import SerialManager
tracemalloc.start()

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(levelname)s:%(name)s:%(funcName)s:[%(lineno)d]   %(message)s'
)


async def listener(e, manager: CanManager, msg: can.Message):
    print(f"{e}: {msg.arbitration_id}")

async def loop(leds: FrontLedArduino):
    while True:
        await asyncio.sleep(5)
        await leds.setTargetColor([255, 0, 0])

        await asyncio.sleep(5)
        await leds.setTargetColor([0, 255, 0])
        await leds.setMaxBrightness(10)

        await asyncio.sleep(5)
        await leds.setTargetColor([0, 0, 255])
        await leds.setMaxBrightness(255)


        await asyncio.sleep(5)
        await leds.setTargetColor([255, 255, 255])


async def main():
    manager = SerialManager()
    leds = FrontLedArduino(manager)

    await asyncio.gather(
        manager.begin(),
        leds.loop(),
        loop(leds)
    )


asyncio.run(main())
