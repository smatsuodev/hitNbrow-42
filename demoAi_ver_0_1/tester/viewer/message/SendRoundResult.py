from viewer.message.BaseMessage import BaseMessage


class SendRoundResult(BaseMessage):
    def __init__(self, winner_player_number: int):
        super().__init__(
            state="in-game",
            message_type="roundResult",
            body={
                "winnerPlayerNumber": winner_player_number
            }
        )
