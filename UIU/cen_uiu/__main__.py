import sys

from cen_uiu.core import UIUCore

from kivy.logger import Logger
_LOGGER = Logger


def main():
    core = UIUCore()

    core.start()

    """ try:
        core.get_process("ui-worker").join()
    except KeyboardInterrupt:
        core.stop() """

    print(core.exit_code)
    return core.exit_code


if __name__ == "__main__":
    sys.exit(main())
