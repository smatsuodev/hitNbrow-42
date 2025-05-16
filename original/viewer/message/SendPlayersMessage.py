from player.Player import Player
from viewer.message.BaseMessage import BaseMessage


class SendPlayersMessage(BaseMessage):
    def __init__(self, player1: Player, player2: Player):
        super().__init__(
            state="matching",
            message_type="sendPlayerName",
            body={
                "players": [
                    {
                        "playerNumber": player1.player_number,
                        "playerName": player1.player_name
                    },
                    {
                        "playerNumber": player2.player_number,
                        "playerName": player2.player_name
                    }
                ]
            }
        )
