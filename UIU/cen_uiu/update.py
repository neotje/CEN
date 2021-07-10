import subprocess
import requests
import threading
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
    process = subprocess.check_output(
        ["git", "pull"], cwd="/home/pi/Github/CEN")

    _LOGGER.info(process.decode('utf-8'))
    return process.decode("utf-8").rfind("up to date") == -1


class UpdateThread(threading.Thread):
    _run: bool

    def __init__(self, core):
        super().__init__()

        self.core = core
        self._run = True

    def run(self):
        try:
            while self._run:
                _LOGGER.info("Checking for updates...")
                if check_for_internet() and update_uiu():
                    _LOGGER.info("Updating...")
                    self.core.restart()

                time.sleep(5)
        except KeyboardInterrupt:
            pass

    def stop(self):
        self._run = False
