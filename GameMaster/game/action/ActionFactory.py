from game.action.ActionType import ActionType
from game.action.BaseAction import BaseAction
from game.action.Challenge import Challenge
from game.action.Change import Change
from game.action.HighLow import HighLow
from game.action.Pass import Pass
from game.action.Shuffle import Shuffle
from game.action.Target import Target
from player.Player import Player


class ActionFactory:

    @classmethod
    def create_action(cls, action_type: ActionType, number: str | None, player: Player) -> BaseAction | Challenge:
        match action_type:
            case ActionType.Challenge:
                return Challenge(player=player, number=number)
            case ActionType.Pass:
                return Pass(player=player)
            case ActionType.Target:
                return Target(player=player, number=number)
            case ActionType.HighLow:
                return HighLow(player=player)
            case ActionType.Change:
                return Change(player=player, number=number)
            case ActionType.Shuffle:
                return Shuffle(player=player, number=number)
            case _:
                raise ValueError()
