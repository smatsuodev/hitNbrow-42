

class ChallengeNumberResponse:
    
    def __init__(self, number):
        self.number = number


    def as_body(self) -> dict:
        return {
            "messageType": 'requestChallengeNumber',
            "body": {
                "action":"call",
                "number": self.number,
            }
        }