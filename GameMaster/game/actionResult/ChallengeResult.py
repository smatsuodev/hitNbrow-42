from game.action.Challenge import Challenge
from game.actionResult.BaseActionResult import BaseActionResult
from util.number_validate import NUMBER_DIGITS


class ChallengeResult(BaseActionResult):
    action: Challenge
    hit: int
    blow: int

    def as_body(self) -> dict:
        return {
            "action": "challenge",
            "playerNumber": self.action.player.player_number,
            "result": {
                "number": self.action.number,
                "hit": self.hit,
                "blow": self.blow
            }
        }

    @property
    def matched(self) -> bool:
        return self.hit >= NUMBER_DIGITS
