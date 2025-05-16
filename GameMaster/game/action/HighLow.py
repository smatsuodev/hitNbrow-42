from typing import TYPE_CHECKING

from game.GameContxt import GameContext
from game.action.ActionType import ActionType
from game.action.BaseAction import BaseAction

if TYPE_CHECKING:
    from game.actionResult.HighLowResult import HighLowResult


class HighLow(BaseAction):
    actionType: ActionType = ActionType.HighLow

    def process_action(self, context: GameContext) -> 'HighLowResult':
        from game.actionResult.HighLowResult import HighLowResult
        player_number = self.player.player_number
        secret = context.get_opponent_secret_number(player_number)
        count = secret.get_high_low_count()
        return HighLowResult(action=self, high=count.high, low=count.low)
