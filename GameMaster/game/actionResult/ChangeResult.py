from game.action.Change import Change
from game.actionResult.BaseActionResult import BaseActionResult


class ChangeResult(BaseActionResult):
    action: Change
    position: int
    is_high: bool

    def as_body(self) -> dict:
        return {
            "action": "change",
            "playerNumber": self.action.player.player_number,
            "result": {
                "position": self.position,
                "high-low": "high" if self.is_high else "low"
            }
        }
