from game.action.Pass import Pass
from game.actionResult.BaseActionResult import BaseActionResult


class PassResult(BaseActionResult):
    action: Pass

    def as_body(self) -> dict:
        return {
            "action": "pass",
            "playerNumber": self.action.player.player_number,
            "result": {}
        }
