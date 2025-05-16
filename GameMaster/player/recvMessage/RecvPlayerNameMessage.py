from typing import Annotated

from pydantic import Field

from player.recvMessage.BaseRecvMessage import BaseRecvMessage, BaseRecvModel
from player.recvMessage.MessageTypes import request_player_name


class PlayerName(BaseRecvModel):
    player_name: Annotated[str, Field(min_length=1, max_length=15)]


class RecvPlayerNameMessage(BaseRecvMessage):
    message_type: Annotated[str, Field(pattern=request_player_name)]
    body: PlayerName
