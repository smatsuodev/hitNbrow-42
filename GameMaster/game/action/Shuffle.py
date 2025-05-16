from typing import TYPE_CHECKING

from game.GameContxt import GameContext
from game.SecretNumber import SecretNumber
from game.action.ActionType import ActionType
from game.action.BaseAction import BaseAction

if TYPE_CHECKING:
    from game.actionResult.ShuffleResult import ShuffleResult


class Shuffle(BaseAction):
    actionType: ActionType = ActionType.Shuffle
    number: str

    def process_action(self, context: GameContext) -> 'ShuffleResult':
        from game.actionResult.ShuffleResult import ShuffleResult
        player_number = self.player.player_number
        secret = context.get_secret_number(player_number)
        if not secret.check_valid_shuffle_number(self.number):
            raise ValueError("invalid changed number")
        context.set_secret_number(player_number, SecretNumber(number=self.number))
        return ShuffleResult(action=self)
