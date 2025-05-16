from typing import TYPE_CHECKING

from game.GameContxt import GameContext
from game.SecretNumber import SecretNumber
from game.action.ActionType import ActionType
from game.action.BaseAction import BaseAction

if TYPE_CHECKING:
    from game.actionResult.ChangeResult import ChangeResult


class Change(BaseAction):
    actionType: ActionType = ActionType.Change
    number: str

    def process_action(self, context: GameContext) -> 'ChangeResult':
        from game.actionResult.ChangeResult import ChangeResult
        player_number = self.player.player_number
        secret = context.get_secret_number(player_number)
        [valid, position, is_high] = secret.check_valid_change_number(self.number)
        if not valid:
            raise ValueError("invalid changed number")
        context.set_secret_number(player_number, SecretNumber(number=self.number))
        return ChangeResult(action=self, position=position, is_high=is_high)
