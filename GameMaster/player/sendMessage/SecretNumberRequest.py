from player.sendMessage.BaseSendMessage import BaseSendMessage


class SecretNumberRequest(BaseSendMessage):
    def __init__(self):
        super().__init__(
            state="start_game",
            message_type="requestSecretNumber",
            body={
                "message": "Please tell your secret number."
            }
        )
