import logging
from aiohttp import web
from cen_uiu import assets

Logger = logging.getLogger(__name__)

STATIC_FOLDER = assets.__path__[0]
INDEX_HTML = assets.__path__[0] + "/index.html"

async def index(request):
    return web.FileResponse(INDEX_HTML)

def create_app() -> web.Application:
    Logger.debug("creating web application")
    app = web.Application(logger=Logger)

    app.router.add_get("/", index, name="index")
    app.router.add_static("/", STATIC_FOLDER)
    web.run_app
    return app

async def run_app(app: web.Application, host: str, port: int):
    Logger.info(f"Starting http server on: {host}:{port}")
    runner = web.AppRunner(app, access_log=Logger)
    await runner.setup()

    site = web.TCPSite(runner, host, port)
    await site.start()
    await site._server.serve_forever()
        
