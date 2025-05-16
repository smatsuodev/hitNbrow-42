package smartscape.co.jp.game.hitandblow.lib.message.to;

import org.java_websocket.client.WebSocketClient;
import smartscape.co.jp.game.hitandblow.lib.message.to.common.ActionBase;
import smartscape.co.jp.game.hitandblow.lib.message.ClientMessage;

import java.io.IOException;

public class CallNumber extends ActionBase {
    String number;
    public CallNumber(WebSocketClient socket, String number) throws IOException {
        super(socket);
        this.number = number;
    }

    @Override
    protected void action() throws Exception {
        try {
            String sendMessage = String.format(ClientMessage.CALL, this.number);
            this.sendMessage(sendMessage);
        } catch (IOException e) {
            throw new Exception();
        }
    }
}
