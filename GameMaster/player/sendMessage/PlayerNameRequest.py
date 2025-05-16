from player.sendMessage.BaseSendMessage import BaseSendMessage


class PlayerNameRequest(BaseSendMessage):
    def __init__(self):
        super().__init__(
            state='connect',
            message_type='requestPlayerName',
            body={
                'message': 'Please declare your player name.'
            }
        )
