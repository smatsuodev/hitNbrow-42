from game.SecretNumber import SecretNumber
from viewer.message.BaseMessage import BaseMessage


class SendSecretNumbers(BaseMessage):
    def __init__(self, p1_secret: SecretNumber, p2_secret: SecretNumber):
        super().__init__(
            state="start-game",
            message_type="sendSecretNumber",
            body={
                "secrets": [
                    {
                        "playerNumber": 1,
                        "number": p1_secret.number
                    },
                    {
                        "playerNumber": 2,
                        "number": p2_secret.number
                    }
                ]
            }
        )
        