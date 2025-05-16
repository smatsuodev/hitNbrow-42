from player.sendMessage.BaseSendMessage import BaseSendMessage


class ChallengeNumberRequest(BaseSendMessage):
    def __init__(self):
        super().__init__(
            state="in-game",
            message_type="requestChallengeNumber",
            body={
                "message": "Please call challenge number."
            }
        )
