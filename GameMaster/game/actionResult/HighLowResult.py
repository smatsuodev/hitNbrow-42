from game.action.HighLow import HighLow
from game.actionResult.BaseActionResult import BaseActionResult


class HighLowResult(BaseActionResult):
    action: HighLow
    high: int
    low: int

    def as_body(self) -> dict:
        return {
            "action": "high-low",
            "playerNumber": self.action.player.player_number,
            "result": {
                "high": self.high,
                "low": self.low
            }
        }