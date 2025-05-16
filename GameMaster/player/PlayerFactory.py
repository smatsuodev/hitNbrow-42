import asyncio
import websockets

from player.Player import Player
from WebsocketServer import WebsocketServer
from player.PlayerNumber import PlayerNumber


class PlayerFactory:
    @staticmethod
    async def create(server: WebsocketServer, player_number: PlayerNumber, loop: asyncio.AbstractEventLoop) -> Player:
        future: asyncio.Future[Player] = loop.create_future()

        def on_connect(socket: websockets.WebSocketServerProtocol):
            player = Player(player_number=player_number, connection=socket)

            print(f'player: {player_number.value} connected')
            future.set_result(player)

        server.set_callback(on_connect)

        try:
            print(f'waiting for player {player_number.value} connection')
            player = await asyncio.wait_for(future, None)
            print(f'player {player_number} was created.')
            return player
        finally:
            server.clear_callback()

