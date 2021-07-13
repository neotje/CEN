import subprocess
import requests
import pathlib

from kivy.clock import Clock

from kivy.logger import Logger
_LOGGER = Logger


def check_for_internet() -> bool:
    try:
        requests.get("http://www.google.com")
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


def update_uiu() -> bool:
    _LOGGER.info("updater: Updating...")

    if not pathlib.Path("/home/pi/Github/CEN").exists():
        _LOGGER.info("updater: Unable to update.")
        return False

    # run git pull and check if anything changed
    output = subprocess.check_output(
        ["git", "pull"], cwd="/home/pi/Github/CEN")

    if output.decode("utf-8").rfind("up to date") == -1:
        return True

    _LOGGER.info("updater: Already up to date.")
    return False


def check_and_update(core, *args):
    if check_for_internet():
        _LOGGER.info("Updater: Checking for updates")

        if update_uiu():
            core.app.switch_to("update")
            
            Clock.schedule_once(core.restart, 5)
