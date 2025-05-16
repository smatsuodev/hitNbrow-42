from player.sendMessage.BaseSendMessage import BaseSendMessage


class ItemActionRequest(BaseSendMessage):
    def __init__(self):
        super().__init__(
            state="in-game",
            message_type="requestItemAction",
            body={
                "message": "Please tell the item you use."
            }
        )
