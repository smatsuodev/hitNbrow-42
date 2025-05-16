from __future__ import annotations
from typing import TYPE_CHECKING

from player.sendMessage.BaseSendMessage import BaseSendMessage

if TYPE_CHECKING:
    from game.actionResult.TargetRsult import TargetResult


class SendTargetResult(BaseSendMessage):
    def __init__(self, result: TargetResult):
        super().__init__(
            state="in-game",
            message_type="itemActionResult-target",
            body=result.as_body()
        )
