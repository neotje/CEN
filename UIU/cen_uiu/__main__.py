import sys

from cen_uiu.core import UIUCore

from kivy.logger import Logger
_LOGGER = Logger

def main():
    core = UIUCore()

    core.start()

    try:
        core._worker.join()
    except KeyboardInterrupt:
        core.stop()

    return core.exit_code


if __name__ == "__main__":
    sys.exit(main())
