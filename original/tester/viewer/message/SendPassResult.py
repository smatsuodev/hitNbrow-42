from __future__ import annotations
from typing import TYPE_CHECKING

from viewer.message.BaseMessage import BaseMessage

if TYPE_CHECKING:
    from game.actionResult.PassResult import PassResult


class SendPassResult(BaseMessage):
    def __init__(self, result: PassResult):
        super().__init__(
            state="in-game",
            message_type="itemActionResult-pass",
            body=result.as_body()
        )
