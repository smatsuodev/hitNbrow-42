from player.sendMessage.BaseSendMessage import BaseSendMessage


class SendPlayerNumber(BaseSendMessage):
    def __init__(self, player_number: int):
        super().__init__(
            state="matching",
            message_type="tellPlayerNumber",
            body={
                'playerNumber': player_number
            }
        )
