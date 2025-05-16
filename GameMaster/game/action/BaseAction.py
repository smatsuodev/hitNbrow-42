from __future__ import annotations
from typing import TYPE_CHECKING

from pydantic import BaseModel

from game.action.ActionType import ActionType
from player.Player import Player

if TYPE_CHECKING:
    from game.GameContxt import GameContext
    from game.actionResult.BaseActionResult import BaseActionResult


class BaseAction(BaseModel):
    actionType: ActionType
    player: Player

    def process_action(self, context: GameContext) -> BaseActionResult:
        raise NotImplementedError()

    class Config:
        arbitrary_types_allowed = True
