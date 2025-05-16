package smartscape.co.jp.game.hitandblow.lib.message.to;

import org.java_websocket.client.WebSocketClient;
import smartscape.co.jp.game.hitandblow.lib.message.ClientMessage;
import smartscape.co.jp.game.hitandblow.lib.message.to.common.ActionBase;

import java.io.IOException;

public class HiLowAction extends ActionBase {

    public HiLowAction(WebSocketClient socket) throws IOException {
        super(socket);
    }
    @Override
    protected void action() throws IOException {
        String sendMessage = String.format(ClientMessage.HIGH_AND_LOW);
        this.sendMessage(sendMessage);
    }
}
