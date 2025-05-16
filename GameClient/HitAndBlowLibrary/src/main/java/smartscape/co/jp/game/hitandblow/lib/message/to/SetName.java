package smartscape.co.jp.game.hitandblow.lib.message.to;

import org.java_websocket.client.WebSocketClient;
import smartscape.co.jp.game.hitandblow.lib.message.to.common.ActionBase;
import smartscape.co.jp.game.hitandblow.lib.message.ClientMessage;

import java.io.IOException;

public class SetName extends ActionBase {
    private final String name;
    public SetName(WebSocketClient socket, String name) throws IOException {
        super(socket);
        this.name = name;
    }
    @Override
    protected void action() throws Exception {
        try {
            String sendMessage = String.format(ClientMessage.SET_NAME,this.name);
            this.sendMessage(sendMessage);
        } catch (IOException e) {
           throw new Exception();
        }
    }
}
