from game.FinishedReason import FinishedReason
from player.Player import Player


class GameFinishedException(Exception):
    def __init__(self, winner: Player | None, reason: FinishedReason, detail: str = ""):
        super().__init__()
        self.winner = winner
        self.reason = reason
        self.detail = detail
