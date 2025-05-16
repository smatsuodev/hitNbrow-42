from __future__ import annotations
from typing import TYPE_CHECKING

from player.sendMessage.BaseSendMessage import BaseSendMessage

if TYPE_CHECKING:
    from game.actionResult.BaseActionResult import BaseActionResult


class SendOpponentActionResult(BaseSendMessage):
    def __init__(self, results: [BaseActionResult]):
        super().__init__(
            state="in-game",
            message_type="opponentActionResult",
            body={
                "actionResults": [result.as_body() for result in results]
            }
        )
