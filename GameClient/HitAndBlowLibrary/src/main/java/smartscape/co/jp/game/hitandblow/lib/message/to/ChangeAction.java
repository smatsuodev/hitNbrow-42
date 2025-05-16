package smartscape.co.jp.game.hitandblow.lib.message.to;

import org.java_websocket.client.WebSocketClient;
import smartscape.co.jp.game.hitandblow.lib.message.ClientMessage;
import smartscape.co.jp.game.hitandblow.lib.message.to.common.ActionBase;

import java.io.IOException;

public class ChangeAction extends ActionBase {

    private final String number;
    public ChangeAction(WebSocketClient socket, String number) throws IOException {
        super(socket);
        this.number = number;
    }
    @Override
    protected void action() throws IOException {
        String sendMessage = String.format(ClientMessage.CHANGE,this.number);
        this.sendMessage(sendMessage);
    }
}
