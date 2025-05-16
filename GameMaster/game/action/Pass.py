from __future__ import annotations
from typing import TYPE_CHECKING

from game.GameContxt import GameContext
from game.action.ActionType import ActionType
from game.action.BaseAction import BaseAction

if TYPE_CHECKING:
    from game.actionResult.PassResult import PassResult


class Pass(BaseAction):
    actionType: ActionType = ActionType.Pass

    def process_action(self, context: GameContext) -> 'PassResult':
        from game.actionResult.PassResult import PassResult
        return PassResult(action=self)
