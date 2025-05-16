from player.PlayerNumber import PlayerNumber
from player.sendMessage.BaseSendMessage import BaseSendMessage


class SendRoundResult(BaseSendMessage):
    def __init__(self, winner_player_number: PlayerNumber):
        super().__init__(
            state="in-game",
            message_type="roundResult",
            body={
                "winnerPlayerNumber": winner_player_number.value
            }
        )
