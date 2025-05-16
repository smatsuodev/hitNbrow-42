from typing import Annotated

from pydantic import Field

from player.recvMessage.BaseRecvMessage import BaseRecvMessage, BaseRecvModel
from player.recvMessage.MessageTypes import request_secret_number
from util.number_validate import validate_number_pattern


class PlayerNumber(BaseRecvModel):
    number: Annotated[str, Field(pattern=validate_number_pattern)]


class RecvSecretNumberMessage(BaseRecvMessage):
    message_type: Annotated[str, Field(pattern=request_secret_number)]
    body: PlayerNumber
