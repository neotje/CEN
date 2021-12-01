import tracemalloc
import can

from cen_uiu.modules.can_bus import CanManager
tracemalloc.start()
import asyncio
from cen_uiu.helpers.event import Event


async def listener(e, manager: CanManager, msg: can.Message):
    print(f"{e}: {msg.arbitration_id}")


async def main():
    manager = CanManager()
    
    await manager.onMessage.listen(listener)
    await manager.listenToId(5, listener)

    await manager.openBus(250_000)



asyncio.run(main())
