import subprocess
import requests
import multiprocessing
import time

from kivy.logger import Logger
_LOGGER = Logger


def check_for_internet() -> bool:
    try:
        requests.get("http://www.google.com")
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


def update_uiu() -> bool:
    output = subprocess.check_output(
        ["git", "pull"], cwd="/home/pi/Github/CEN")

    _LOGGER.info(output.decode('utf-8'))

    if output.decode("utf-8").rfind("up to date") == -1:
        output = subprocess.check_output(
            ["scripts/setup"], cwd="/home/pi/Github/CEN/UIU")
        return True
    return False


class UpdateThread(multiprocessing.Process):
    _run: bool

    def __init__(self, core):
        super().__init__(name="update-worker")

        self.core = core
        self._run = True

    def run(self):
        while self._run:
            _LOGGER.info("Checking for updates...")
            if check_for_internet() and update_uiu():
                _LOGGER.info("Updating...")
                self.core.restart()
                break

            time.sleep(60)

    def kill(self) -> None:
        self._run = False
        return super().terminate()