

class SecretNumberResponse:
    
    def __init__(self, number):
        self.number = number


    def as_body(self) -> dict:
        return {
            "messageType": 'requestSecretNumber',
            "body": {
                "number": self.number,
            }
        }