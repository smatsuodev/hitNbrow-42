from __future__ import annotations
from typing import TYPE_CHECKING

from game.GameContxt import GameContext
from game.action.ActionType import ActionType
from game.action.BaseAction import BaseAction

if TYPE_CHECKING:
    from game.actionResult.ChallengeResult import ChallengeResult


class Challenge(BaseAction):
    actionType: ActionType = ActionType.Challenge
    number: str

    def process_action(self, context: GameContext) -> 'ChallengeResult':
        from game.actionResult.ChallengeResult import ChallengeResult
        secret = context.get_opponent_secret_number(self.player.player_number)
        count = secret.get_hit_blow_count(self.number)
        return ChallengeResult(action=self, hit=count.hit, blow=count.blow)
