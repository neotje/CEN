import sys

from cen_uiu.core import UIUCore

from kivy.logger import Logger
_LOGGER = Logger

exit_code = 0

def main():
    core = UIUCore()

    core.start()

    try:
        core._worker.join()
    except KeyboardInterrupt:
        core.stop()

    global exit_code
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
