# TODO: create a settings manager.

import asyncio
import json
from os.path import exists
from typing import Any, List
from cen_uiu import config

CONFIG_FILE = config.__path__[0] + "/main.json"


async def checkConfigFile():
    loop = asyncio.get_running_loop()

    if not exists(CONFIG_FILE):
        config = await loop.run_in_executor(None, open, CONFIG_FILE, 'w')
        return await loop.run_in_executor(None, json.dump, {}, config)            


async def getAll() -> dict:
    await checkConfigFile()
    loop = asyncio.get_running_loop()

    config = await loop.run_in_executor(None, open, CONFIG_FILE)
    return await loop.run_in_executor(None, json.load, config)  


async def setAll(data: dict):
    await checkConfigFile()
    loop = asyncio.get_running_loop()

    config = await loop.run_in_executor(None, open, CONFIG_FILE, 'w')
    await loop.run_in_executor(None, json.dump, data, config)


async def get(key: str):
    return (await getAll()).get(key)


async def set(key: str, val: Any):
    data = await getAll()
    data[key] = val
    await setAll(data)