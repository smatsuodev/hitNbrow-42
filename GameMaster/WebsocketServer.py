from typing import Optional, Callable

import asyncio
import websockets
from websockets import ServerConnection

DOMAIN = 'localhost'
PORT = 8088


class WebsocketServer:
    def __init__(self, loop: asyncio.AbstractEventLoop, *, domain: str = DOMAIN, port: int = PORT):
        self._loop = loop
        self.__server: Optional[websockets.WebSocketServer] = None
        self.__ws_connect_callback = None
        self.__server_loop = asyncio.new_event_loop()
        self.__domain = domain
        self.__port = port

    def __del__(self):
        self.stop()

    async def start(self):
        async def on_connect(websocket: ServerConnection):
            # print(f'on_connect {websocket}')
            if self.__ws_connect_callback:
                self._loop.run_in_executor(None, self.__ws_connect_callback, websocket)
                await self._loop.create_future()

        self.__server = await websockets.serve(on_connect, self.__domain, self.__port)

    def stop(self):
        self.__server.close()

    def set_callback(self, on_connect: Callable[[ServerConnection, ], None]):
        self.__ws_connect_callback = on_connect

    def clear_callback(self):
        self.__ws_connect_callback = None

    def server_url(self) -> str:
        return f'ws://{self.__domain}:{self.__port}'
