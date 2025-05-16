import re
from typing import Annotated

from pydantic import Field, model_validator
from typing_extensions import Self

from player.recvMessage.BaseRecvMessage import BaseRecvMessage, BaseRecvModel
from player.recvMessage.MessageTypes import request_item_action, item_action
from util.number_validate import validate_number_pattern, validate_single_number_pattern


class ActionBody(BaseRecvModel):
    action: Annotated[str, Field(pattern=item_action)]
    number: str | None = None

    @model_validator(mode='after')
    def validate_number(self) -> Self:
        match self.action:
            case "target":
                if re.match(validate_single_number_pattern, self.number) is None:
                    raise ValueError("invalid number")
            case "shuffle" | "change":
                if re.match(validate_number_pattern, self.number) is None:
                    raise ValueError("invalid number")
        return self


class RecvItemActionMessage(BaseRecvMessage):
    message_type: Annotated[str, Field(pattern=request_item_action)]
    body: ActionBody

    @model_validator(mode='after')
    def validate_action(self) -> Self:
        if str.split(self.message_type, "-", 1)[1] != self.body.action:
            raise ValueError("invalid action set")
        return self
