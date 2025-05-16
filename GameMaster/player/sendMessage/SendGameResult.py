from player.PlayerNumber import PlayerNumber
from player.sendMessage.BaseSendMessage import BaseSendMessage


class SendGameResult(BaseSendMessage):
    def __init__(self, winner_player_number: PlayerNumber | None):
        super().__init__(
            state="finish-game",
            message_type="gameResult",
            body={
                "winnerPlayerNumber": winner_player_number.value if winner_player_number is not None else 0
            }
        )
