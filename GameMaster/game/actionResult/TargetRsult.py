from game.action.Target import Target
from game.actionResult.BaseActionResult import BaseActionResult


class TargetResult(BaseActionResult):
    action: Target
    position: int

    def as_body(self) -> dict:
        return {
            "action": "target",
            "playerNumber": self.action.player.player_number,
            "result": {
                "number": self.action.number,
                "position": self.position
            }
        }
