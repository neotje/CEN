import sys
from cen_uiu.app import UIUApp

import logging
logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG,
    format='%(levelname)s:%(name)s:%(funcName)s:[%(lineno)d]   %(message)s'
)
_LOGGER = logging.getLogger(__name__)


def main():
    app = UIUApp()

    app.run()


if __name__ == "__main__":
    sys.exit(main())