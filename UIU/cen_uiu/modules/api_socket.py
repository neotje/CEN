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
    def __init__(self, js_api) -> None:
        self._server = websockets.serve(self._handler, "127.0.0.1", 2888)
        self._js_api = js_api
        self._loop = asyncio.new_event_loop()

        asyncio.set_event_loop(self._loop)

    def serve(self):
        self._loop.run_until_complete(self._server)
        self._loop.run_forever()

    def close(self):
        self._server.close()
        self._loop.stop()

    async def _handler(self, websocket, path):
        # get all function of the js_api object.
        method_list = inspect.getmembers(self._js_api, predicate=inspect.ismethod)

        # send list of methods to client.
        # using the expose action for every function.
        for m in method_list:
            methodName = m[0]
            methodParams = list(inspect.getfullargspec(m[1].args))

            if not isBuiltinFunc(methodName):
                sendObj = {
                    "action": "expose",
                    "name": methodName,
                    "params": methodParams
                }
                await websocket.send(json.dumps(sendObj))

        # send ready action to the client.
        await websocket.send(json.dumps({"action": "ready"}))

        while websocket.open:
            msg = await websocket.recv()
            
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
                    "content": "{}"
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

        """ websocket.close()
        await websocket.wait_closed() """
