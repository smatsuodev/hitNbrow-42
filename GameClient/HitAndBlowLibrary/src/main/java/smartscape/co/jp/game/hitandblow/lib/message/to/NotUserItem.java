package smartscape.co.jp.game.hitandblow.lib.message.to;

import org.java_websocket.client.WebSocketClient;
import smartscape.co.jp.game.hitandblow.lib.message.to.common.ActionBase;
import smartscape.co.jp.game.hitandblow.lib.message.ClientMessage;

import java.io.IOException;

public class NotUserItem extends ActionBase {

    public NotUserItem(WebSocketClient socket) throws IOException {
        super(socket);
    }
    @Override
    protected void action() throws Exception {
        try {
            String sendMessage = String.format(ClientMessage.NOT_USE_ITEM);
            this.sendMessage(sendMessage);
        } catch (IOException e) {
            throw new Exception();
        }
    }
}
