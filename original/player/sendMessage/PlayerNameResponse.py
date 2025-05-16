

class PlayerNameResponse:
    
    def __init__(self, name):
        self.name = name


    def as_body(self) -> dict:
        return {
            "messageType": 'requestPlayerName',
            "body": {
                "playerName": self.name,
            }
        }