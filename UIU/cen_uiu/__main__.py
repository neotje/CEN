import logging
import webview
from cen_uiu.modules.api_socket import ApiSocket
from cen_uiu import api, assets
import asyncio
import sys
import argparse
from aiohttp import web

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
    parser = argparse.ArgumentParser(prog="uiu-backend")
    parser.add_argument('-p', "--port", type=int,
                        help="socket server port", default=2888, required=False)
    parser.add_argument('-d', "--debug", help="enable debug level logging and inspector", required=False, action='store_true')
    args = parser.parse_args()

    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG if args.debug else logging.INFO,
        format='%(levelname)s:%(name)s:%(funcName)s:[%(lineno)d]   %(message)s'
    )
    Logger.debug("Debug logging.")

    apiObj = api.UIUapi()
    apiSocket = ApiSocket(apiObj, args.port)

    try:
        #asyncio.run(apiSocket.serve())
        asyncio.run(run_backend(apiSocket))
    except KeyboardInterrupt:
        pass

async def run_backend(socket: ApiSocket):
    app = web.Application(logger=Logger)
    app.router.add_static("/", path=assets.__path__[0], name='root')
    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, 'localhost', 4123)
    await site.start()

    await socket.serve()
    await runner.cleanup()


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
