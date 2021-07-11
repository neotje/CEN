import sys

from cen_uiu.core import UIUCore

from kivy.logger import Logger
_LOGGER = Logger

def main():
    core = UIUCore()

    core.start()

    try:
        core.get_process("ui-worker").join()
    except KeyboardInterrupt:
        core.stop()

    print(core.exit_code.value)
    exit(int(core.exit_code.value))


if __name__ == "__main__":
    sys.exit(main())
