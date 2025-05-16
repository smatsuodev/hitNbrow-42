import asyncio

from websockets import ServerConnection, State

from WebsocketServer import WebsocketServer
from game.GameContxt import GameContext
from game.actionResult.BaseActionResult import BaseActionResult
from player.PlayerNumber import PlayerNumber
from viewer.message.ActionResultFactory import ActionResultFactory
from viewer.message.BaseMessage import BaseMessage
from viewer.message.SendGameResuot import SendGameResult
from viewer.message.SendPlayersMessage import SendPlayersMessage
from viewer.message.SendRoundResult import SendRoundResult
from viewer.message.SendSecretNumbers import SendSecretNumbers


class Viewer:

    def __init__(self):
        self.__connection: ServerConnection | None = None
        self.__loop = None

    @property
    def connected(self) -> bool:
        return self.__connection is not None and self.__connection.state == State.OPEN

    def wait_for_connection(self, server: WebsocketServer, loop: asyncio.AbstractEventLoop):
        self.__loop = loop

        def on_connect(socket: ServerConnection):
            self.__connection = socket

            print('viewer connected.')

        server.set_callback(on_connect)
        print('waiting for viewer connection')

    async def send(self, message: BaseMessage):
        if self.connected:
            # print("viewer send: " + message.json())
            await self.__connection.send(message.json())

    async def send_players(self, context: GameContext):
        await self.send(
            SendPlayersMessage(
                player1=context.get_player(PlayerNumber.Player1),
                player2=context.get_player(PlayerNumber.Player2)
            )
        )

    async def send_secret_numbers(self, context: GameContext):
        await self.send(
            SendSecretNumbers(
                p1_secret=context.get_secret_number(PlayerNumber.Player1),
                p2_secret=context.get_secret_number(PlayerNumber.Player2)
            )
        )

    async def send_action_result(self, result: BaseActionResult, context: GameContext):
        message = ActionResultFactory.create_from(result)
        await self.send(message)

    async def send_round_result(self, winner_player_number: PlayerNumber, context: GameContext):
        await self.send(
            SendRoundResult(
                winner_player_number=winner_player_number.value
            )
        )

    async def send_game_result(self, winner_player_number: PlayerNumber, context: GameContext):
        await self.send(
            SendGameResult(
                winner_player_number=winner_player_number.value
            )
        )
