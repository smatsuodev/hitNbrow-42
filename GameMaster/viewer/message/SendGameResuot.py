from viewer.message.BaseMessage import BaseMessage


class SendGameResult(BaseMessage):
    def __init__(self, winner_player_number: int):
        super().__init__(
            state="finish-game",
            message_type="gameResult",
            body={
                "winnerPlayerNumber": winner_player_number
            }
        )
