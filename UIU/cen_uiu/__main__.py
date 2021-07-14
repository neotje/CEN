import logging
import sys

from cen_uiu.core import UIUCore

from kivy.logger import Logger
_LOGGER = Logger

Logger.setLevel(logging.DEBUG)


def main():
    core = UIUCore()

    core.start()

    print(core.exit_code)
    return core.exit_code


if __name__ == "__main__":
    sys.exit(main())
