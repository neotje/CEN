import tracemalloc

tracemalloc.start()

import sys
import asyncio

from cen_uiu import api, assets
from cen_uiu.modules.api_socket import ApiSocket
from cen_uiu.modules.bluetooth import discover_and_connect
from cen_uiu.helpers import env

import webview

import logging

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(funcName)s:[%(lineno)d]   %(message)s'
)
Logger = logging.getLogger(__name__)



DEBUG_SERVER = "http://localhost:3000"

WINDOW_TITLE = "Matiz UIU"
INDEX_HTML = assets.__path__[0] + "/index.html"

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

        window.evaluate_js("""
        document.addEventListener('keypress', (e) => {
            if(e.code == 'KeyQ') {
                window.uiu.api.quit();
            }
            if(e.code == 'KeyF') {
                window.uiu.api.toggle_fullscreen();
            }
        });
        """)

    discover_and_connect(BLUETOOTH_ADAPTER)

    apiSocket.serve()

    for window in webview.windows:
        window.destroy()


async def run():
    env.setup()

    debug = env.getBool(env.UIU_DEBUG)
    withoutUI = env.getBool(env.UIU_WITHOUT_UI)
    uiSrc = env.getStr(env.UIU_UI_SERVER)
    fullscreen = env.getBool(env.UIU_FULLSCREEN)

    socketTask = asyncio.create_task(apiSocket.serve())

    if withoutUI:
        await socketTask
        return 0

    if uiSrc == "":
        uiSrc = INDEX_HTML

    try:
        webview.create_window(WINDOW_TITLE, uiSrc, fullscreen=fullscreen)
        webview.start(webviewStart, http_server=True, debug=debug)
    except KeyboardInterrupt:
        pass
    
    for window in webview.windows:
        window.destroy()

    await socketTask
    return 0


def main():
    try:
        code = asyncio.run(run())
    except KeyboardInterrupt:
        return 0
    return code


if __name__ == "__main__":
    sys.exit(main())
