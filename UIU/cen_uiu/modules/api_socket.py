import asyncio
import websockets
import inspect
import json
import traceback

import logging
Logger = logging.getLogger(__name__)

class ApiSocket:
    def __init__(self, js_api) -> None:
        asyncio.set_event_loop(asyncio.new_event_loop())
        self._server = websockets.serve(self._handler, "127.0.0.1", 2888)
        self._js_api = js_api

    def serve(self):
        asyncio.get_event_loop().run_until_complete(self._server)
        asyncio.get_event_loop().run_forever()

    def close(self):
        self._server.close()
        asyncio.get_event_loop().stop()

    async def _handler(self, websocket, path):
        Logger.info(path)
        method_list = inspect.getmembers(
            self._js_api, predicate=inspect.ismethod)
        method_list = [
            m for m in method_list if m[0].startswith("__") is False
        ]
        method_list = [
            {
                "func": m[0],

                "params": list(inspect.getfullargspec(m[1]).args)
            }
            for m in method_list
        ]

        for m in method_list:
            params = [p for p in m["params"] if not p == "self"]
            obj = {
                "action": "expose",
                "name": m["func"],
                "params": params
            }
            await websocket.send(json.dumps(obj))

        await websocket.send(json.dumps({"action": "ready"}))

        while websocket.open:
            msg = await websocket.recv()
            Logger.debug(msg)

            content = json.loads(msg)

            if content['action'] == "call":
                funcName = content['function']
                params = list(content['params'].values())
                id = content['id']

                data = {
                    "action": "return",
                    "id": id,
                    "function": funcName,
                    "isError": False,
                    "content": "{}"
                }

                try:
                    result = getattr(self._js_api, funcName)(*params)
                    data["content"] = result
                except Exception as e:
                    data["content"] = {
                        "message": str(e),
                        "name": type(e).__name__,
                        "stack": traceback.format_exc()
                    }
                    data["isError"] = True
                finally:
                    Logger.debug(data)
                    await websocket.send(json.dumps(data))

        websocket.close()
        await websocket.wait_closed()



