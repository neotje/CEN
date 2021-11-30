import logging
from cen_uiu.http_server import create_app, run_app
from cen_uiu.modules.bluetooth import discover_and_connect
import webview
from cen_uiu.modules.api_socket import ApiSocket
from cen_uiu import api, assets
import asyncio
import sys
import argparse

Logger = logging.getLogger(__name__)

WINDOW_TITLE = "Matiz UIU"
INDEX_HTML = assets.__path__[0] + "/index.html"
BLUETOOTH_ADAPTER = "hci0"

def webviewStart():
    Logger.info("webview started")

    for window in webview.windows:
        Logger.debug(window.get_current_url())

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


def backend():
    try:
        asyncio.run(run_backend())
    except KeyboardInterrupt:
        pass


async def run_backend():
    parser = argparse.ArgumentParser(prog="uiu-backend")
    parser.add_argument('-p', "--port", type=int,
                        help="socket server port", default=2888, required=False)
    parser.add_argument('-d', "--debug", help="enable debug level logging and inspector", required=False, action='store_true')
    parser.add_argument('--nohttp', help="disable http server for hosting the frontend files", required=False, action='store_true')
    parser.add_argument("--http_port", type=int, help="http server port", default=4123, required=False)
    parser.add_argument("--http_host", type=str, help="http server port", default="localhost", required=False)
    args = parser.parse_args()

    apiObj = api.UIUapi()
    apiSocket = ApiSocket(apiObj, args.port)
    
    frontendApp = create_app()

    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG if args.debug else logging.INFO,
        format='%(levelname)s:%(name)s:%(funcName)s:[%(lineno)d]   %(message)s'
    )
    Logger.debug("Debug logging.")

    routines = [
        apiSocket.serve(),
        discover_and_connect("hci0")
    ]

    if not args.nohttp:
        routines.append(run_app(frontendApp, args.http_host, args.http_port))

    await asyncio.gather(
        *routines
    )


def frontend():
    parser = argparse.ArgumentParser(prog="uiu-frontend")
    parser.add_argument('-d', "--debug", help="enable debug level logging and inspector", required=False, action='store_true')
    parser.add_argument("--html", type=str, help="path to html file",
                        default=INDEX_HTML, required=False)
    parser.add_argument("-w", "--windowed", help="enable windowed mode", required=False, action='store_true')
    args = parser.parse_args()

    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG if args.debug else logging.INFO,
        format='%(levelname)s:%(name)s:%(funcName)s:[%(lineno)d]   %(message)s'
    )

    try:
        webview.create_window(WINDOW_TITLE, args.html, fullscreen=not args.windowed)
        webview.start(webviewStart, http_server=True, debug=args.debug)
    except KeyboardInterrupt:
        pass
