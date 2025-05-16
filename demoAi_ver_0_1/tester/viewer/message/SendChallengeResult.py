from __future__ import annotations
from typing import TYPE_CHECKING

from viewer.message.BaseMessage import BaseMessage

if TYPE_CHECKING:
    from game.actionResult import ChallengeResult


class SendChallengeResult(BaseMessage):
    def __init__(self, result: ChallengeResult):
        super().__init__(
            state="in-game",
            message_type="challengeResult",
            body=result.as_body()
        )
