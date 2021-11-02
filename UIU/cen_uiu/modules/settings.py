# TODO: create a settings manager.

import json
from os.path import exists
from typing import Any, List
from cen_uiu import config

CONFIG_FILE = config.__path__[0] + "/main.json"


def checkConfigFile():
    if not exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as config:
            json.dump({}, config)


def getAll() -> dict:
    checkConfigFile()

    with open(CONFIG_FILE) as config:
        return json.load(config)


def setAll(data: dict):
    checkConfigFile()

    with open(CONFIG_FILE, 'w') as config:
        json.dump(data, config)


def get(key: str):
    return getAll().get(key)


def set(key: str, val: Any):
    data = getAll()
    data[key] = val
    setAll(data)