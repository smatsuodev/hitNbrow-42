from __future__ import annotations
from typing import TYPE_CHECKING

from player.sendMessage.BaseSendMessage import BaseSendMessage

if TYPE_CHECKING:
    from game.actionResult.HighLowResult import HighLowResult


class SendHighLowResult(BaseSendMessage):
    def __init__(self, result: HighLowResult):
        super().__init__(
            state="in-game",
            message_type="itemActionResult-high-low",
            body=result.as_body()
        )
