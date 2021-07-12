import subprocess
from cen_uiu.helpers.task import Task
import requests
import asyncio
import pathlib

from kivy.logger import Logger
_LOGGER = Logger


def check_for_internet() -> bool:
    try:
        requests.get("http://www.google.com")
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


def update_uiu() -> bool:
    _LOGGER.info("UpdaterTask: Updating...")

    if not pathlib.Path("/home/pi/Github/CEN").exists():
        return False
    
    output = subprocess.check_output(
        ["git", "pull"], cwd="/home/pi/Github/CEN")

    _LOGGER.info(output.decode('utf-8'))

    if output.decode("utf-8").rfind("up to date") == -1:
        output = subprocess.check_output(
            ["scripts/setup"], cwd="/home/pi/Github/CEN/UIU")
        return True
    return False


class UpdaterTask(Task):
    _run: bool

    def __init__(self, core):
        self.core = core
        self._run = True

    async def async_run(self):
        while self._run:
            _LOGGER.info("UpdaterTask: Checking for updates...")
            if check_for_internet() and update_uiu():
                self.core.restart()
                break

            await asyncio.sleep(60)