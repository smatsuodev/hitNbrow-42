from __future__ import annotations
from typing import TYPE_CHECKING

from player.sendMessage.BaseSendMessage import BaseSendMessage

if TYPE_CHECKING:
    from game.actionResult.ChangeResult import ChangeResult


class SendChangeResult(BaseSendMessage):
    def __init__(self, result: ChangeResult):
        super().__init__(
            state="in-game",
            message_type="itemActionResult-change",
            body=result.as_body()
        )
