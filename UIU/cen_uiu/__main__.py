import os
import sys
import subprocess

from cen_uiu import api, assets
from cen_uiu.modules.api_socket import ApiSocket
from cen_uiu.modules.bluetooth import discover_and_connect

import webview

import logging

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(funcName)s:[%(lineno)d]   %(message)s'
)
Logger = logging.getLogger(__name__)

ENV_UIU_DEBUG = "UIU_DEBUG"
DEBUG_SERVER = "http://localhost:3000"

WINDOW_TITLE = "Matiz UIU"
INDEX_HTML = assets.__path__[0] + "./index.html"

BLUETOOTH_ADAPTER = "hci0"

apiSocket = ApiSocket(api.UIUapi())


def webviewStart():
    Logger.info("webview started")

    def webviewClosed():
        apiSocket._js_api.bl_disable_audio()
        apiSocket.close()

    for window in webview.windows:
        Logger.info(window.get_current_url())
        window.closed += webviewClosed

    discover_and_connect(BLUETOOTH_ADAPTER)

    apiSocket.serve()


def main():
    debug = True if str(os.environ.get(ENV_UIU_DEBUG)).capitalize() == "TRUE" else False

    if debug:
        w = webview.create_window(
            WINDOW_TITLE, DEBUG_SERVER, fullscreen=False, minimized=False)
    else:
        Logger.info(INDEX_HTML)
        w = webview.create_window(WINDOW_TITLE, INDEX_HTML, fullscreen=True)

    webview.start(webviewStart, http_server=True, debug=debug)
    return 0


if __name__ == "__main__":
    sys.exit(main())
