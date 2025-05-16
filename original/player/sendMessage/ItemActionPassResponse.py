

class ItemActionPassResponse:
    
    def as_body(self) -> dict:
        return {
            "messageType": 'requestItemAction-pass',
            "body": {
                "action": "pass",
            }
        }