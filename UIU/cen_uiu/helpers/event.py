import asyncio
from typing import List

class Event:
    _name: str
    _tasks: List[asyncio.Task]
    _listeners: List

    def __init__(self, name: str) -> None:
        self._name = name
        self._tasks = []
        self._listeners = []

    async def dispatch(self, *args):
        for l in self._listeners:
            self._tasks.append(asyncio.create_task(l(self._name, *args)))

    def listen(self, listener):
        self._listeners.append(listener)

    async def remove(self, listener):
        try:
            self._listeners.remove(listener)
        except ValueError:
            pass

    