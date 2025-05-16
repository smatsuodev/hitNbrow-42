from typing import TYPE_CHECKING

from game.GameContxt import GameContext
from game.action.ActionType import ActionType
from game.action.BaseAction import BaseAction

if TYPE_CHECKING:
    from game.actionResult.TargetRsult import TargetResult


class Target(BaseAction):
    actionType: ActionType = ActionType.Target
    number: str

    def process_action(self, context: GameContext) -> 'TargetResult':
        from game.actionResult.TargetRsult import TargetResult
        secret = context.get_opponent_secret_number(self.player.player_number)
        index = secret.get_number_index(self.number)
        return TargetResult(action=self, position=index)
