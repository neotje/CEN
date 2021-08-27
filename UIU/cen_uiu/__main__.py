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


def webviewStart():
    Logger.info("webview started")

    s = ApiSocket(api.UIUapi())
    s.serve()

    def webviewClosed():
        s._js_api.bl_disable_audio()
        s.close()

    for w in webview.windows:
        print(w.get_current_url())
        w.closed += webviewClosed

    discover_and_connect("hci0")


def main():
    debug = False

    if debug:
        w = webview.create_window(
            "Matiz UIU", "http://localhost:3000", fullscreen=False, minimized=False)
    else:
        w = webview.create_window("Matiz UIU", assets.__path__[
                                  0] + "/index.html", fullscreen=True)

    webview.start(webviewStart, http_server=True, debug=debug)
    return 0


if __name__ == "__main__":
    sys.exit(main())
