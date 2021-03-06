import asyncio
import websockets
import inspect
import json
import traceback

import logging
Logger = logging.getLogger(__name__)


def isBuiltinFunc(funcName: str) -> bool:
    return funcName.startswith("__")


class ApiSocket:
    def __init__(self, js_api, port=2888) -> None:
        self.port = port
        self._js_api = js_api

    async def serve(self):
        self._server = websockets.serve(self._handler, "127.0.0.1", self.port)

        await self._js_api._setup()
        
        async with self._server:
            await asyncio.Future()

    def close(self):
        self._server.close()

    async def _handler(self, websocket, path):
        Logger.info("Someone is connected...")
        # get all function of the js_api object.
        method_list = inspect.getmembers(
            self._js_api, predicate=inspect.ismethod)

        # send list of methods to client.
        # using the expose action for every function.
        for m in method_list:
            methodName = m[0]
            methodParams = list(inspect.getfullargspec(m[1]).args)

            if not isBuiltinFunc(methodName):
                sendObj = {
                    "action": "expose",
                    "name": methodName,
                    "params": methodParams
                }
                await websocket.send(json.dumps(sendObj))

        # send ready action to the client.
        await websocket.send(json.dumps({"action": "ready"}))
        
        try:
            async for msg in websocket:
                Logger.debug(msg)

                # decode message from the client.
                content = json.loads(msg)

                # call function by name.
                if content['action'] == "call":
                    methodName = content['function']
                    methodParams = list(content['params'].values())
                    resultId = content['id']

                    # data to return
                    data = {
                        "action": "return",
                        "id": resultId,
                        "function": methodName,
                        "isError": False,
                        "content": {}
                    }

                    try:
                        result = await getattr(self._js_api, methodName)(*methodParams)
                        data["content"] = result
                    except Exception as e:
                        # send error info on exception
                        data["content"] = {
                            "message": str(e),
                            "name": type(e).__name__,
                            "stack": traceback.format_exc()
                        }
                        data["isError"] = True
                    finally:
                        Logger.debug(data)
                        await websocket.send(json.dumps(data))

        except Exception:
            pass
        await websocket.close()
        """ websocket.close()
        await websocket.wait_closed() """
