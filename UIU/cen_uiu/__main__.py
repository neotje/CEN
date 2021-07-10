import sys
from cen_uiu.app import UIUApp
from cen_uiu.modules.audio import BluetoothInput

import logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(levelname)s:%(name)s:%(funcName)s:[%(lineno)d]   %(message)s'
)
_LOGGER = logging.getLogger(__name__)


def main():
    bl = BluetoothInput()

    bl.enable()

    app = UIUApp()

    try:
        app.run()
    except KeyboardInterrupt:
        pass
    finally:
        app.stop()
        bl.disable()
    

if __name__ == "__main__":
    sys.exit(main())