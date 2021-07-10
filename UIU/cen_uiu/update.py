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
    try:
        process = subprocess.run(
            ["git", "pull"], cwd="/home/Pi/Github/CEN", capture_output=True)

        return process.stdout.rfind("Already up to date.") == -1

    except Exception:
        return False


class UpdateThread(threading.Thread):
    _run: bool

    def __init__(self, core):
        super().__init__()

        self.core = core
        self._run = True

    def run(self):
        try:
            while self._run:
                if check_for_internet() and update_uiu():
                    self.core.restart()

                time.sleep(5)
        except KeyboardInterrupt:
            pass

    def stop(self):
        self._run = False
