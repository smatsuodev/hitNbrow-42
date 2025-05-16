from player.PlayerNumber import PlayerNumber


FINISH_POINT = 3


class Score:
    def __init__(self):
        self.__p1_score = 0
        self.__p2_score = 0

    @property
    def player1_score(self) -> int:
        return self.__p1_score

    @property
    def player2_score(self) -> int:
        return self.__p2_score

    def add_score(self, winner: PlayerNumber):
        if winner == PlayerNumber.Player1:
            self.__p1_score += 1
        else:
            self.__p2_score += 1

    def get_winner(self) -> PlayerNumber | None:
        if self.__p1_score > self.__p2_score:
            return PlayerNumber.Player1
        elif self.__p1_score < self.__p2_score:
            return PlayerNumber.Player2
        else:
            return None
