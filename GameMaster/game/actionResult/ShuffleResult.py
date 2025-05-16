from game.action.Shuffle import Shuffle
from game.actionResult.BaseActionResult import BaseActionResult


class ShuffleResult(BaseActionResult):
    action: Shuffle

    def as_body(self) -> dict:
        return {
            "action": "shuffle",
            "playerNumber": self.action.player.player_number,
            "result": {}
        }
