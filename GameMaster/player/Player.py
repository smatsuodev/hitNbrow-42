from __future__ import annotations

import json
from typing import List, Tuple, TYPE_CHECKING, Any

from pydantic import BaseModel
from websockets import ServerConnection

from game.action.ActionType import ActionType
from player.PlayerNumber import PlayerNumber
from player.recvMessage.RecvChallengeNumberMessage import RecvChallengeNumberMessage
from player.recvMessage.RecvItemActionMessage import RecvItemActionMessage
from player.recvMessage.RecvPlayerNameMessage import RecvPlayerNameMessage
from player.recvMessage.RecvSecretNumberMessage import RecvSecretNumberMessage
from player.sendMessage.ChallengeNumberRequest import ChallengeNumberRequest
from player.sendMessage.ItemActionRequest import ItemActionRequest
from player.sendMessage.BaseSendMessage import BaseSendMessage
from player.sendMessage.PlayerNameRequest import PlayerNameRequest
from player.sendMessage.SecretNumberRequest import SecretNumberRequest
from player.sendMessage.SendGameResult import SendGameResult
from player.sendMessage.SendOpponentActionResult import SendOpponentActionResult
from player.sendMessage.SendPlayerNumber import SendPlayerNumber
from player.sendMessage.SendRoundResult import SendRoundResult

if TYPE_CHECKING:
    from game.actionResult.BaseActionResult import BaseActionResult

DEBUG = False


class Player(BaseModel):
    player_number: PlayerNumber
    player_name: str | None = None
    active: bool = True
    connection: ServerConnection

    class Config:
        arbitrary_types_allowed = True

    async def send_message(self, message: BaseSendMessage):
        if DEBUG:
            print("send: " + message.json())
        await self.connection.send(message.json())

    async def send_message_with_response(self, message: BaseSendMessage):
        if DEBUG:
            print("send: " + message.json())
        await self.connection.send(message.json())
        return await self.recv_input()

    async def recv_input(self) -> dict:
        player_message = await self.connection.recv()
        if DEBUG:
            print("receive: " + player_message)
        return json.loads(player_message)

    async def send_player_number(self):
        await self.send_message(SendPlayerNumber(player_number=self.player_number.value))

    async def request_player_name(self) -> str:
        res_json = await self.send_message_with_response(PlayerNameRequest())
        response = RecvPlayerNameMessage(**res_json)
        return response.body.player_name

    async def request_secret_number(self) -> str:
        res_json = await self.send_message_with_response(SecretNumberRequest())
        response = RecvSecretNumberMessage(**res_json)
        return response.body.number

    async def request_challenge_number(self) -> str:
        res_json = await self.send_message_with_response(ChallengeNumberRequest())
        response = RecvChallengeNumberMessage(**res_json)
        return response.body.number

    async def request_item_action(self) -> Tuple[ActionType, str | None]:
        res_json = await self.send_message_with_response(ItemActionRequest())
        response = RecvItemActionMessage(**res_json)
        return ActionType(response.body.action), response.body.number

    async def send_action_result(self, result: BaseActionResult):
        from player.sendMessage.ActionResultFactory import ActionResultFactory
        await self.send_message(ActionResultFactory.create_from(result))

    async def send_opponent_action_results(self, results: List[BaseActionResult]):
        await self.send_message(SendOpponentActionResult(results=results))

    async def send_round_result(self, winner_player_number: PlayerNumber):
        await self.send_message(SendRoundResult(winner_player_number=winner_player_number))

    async def send_game_result(self, winner_player_number: PlayerNumber | None):
        await self.send_message(SendGameResult(winner_player_number=winner_player_number))
