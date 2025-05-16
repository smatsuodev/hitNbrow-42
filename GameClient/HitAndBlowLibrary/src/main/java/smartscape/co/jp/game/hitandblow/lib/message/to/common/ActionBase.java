package smartscape.co.jp.game.hitandblow.lib.message.to.common;

import com.fasterxml.jackson.core.JsonProcessingException;
import org.java_websocket.client.WebSocketClient;

import java.io.*;

public abstract class ActionBase extends Thread{
    protected WebSocketClient socket;
    public ActionBase(WebSocketClient socket) throws IOException {
        this.socket = socket;
    }
    public interface ActionCallBack {
        void onComplete(String res);
    }

    @Override
    public void run() {
        super.run();
        try {
            this.action();
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    protected void sendMessage(String message) throws IOException {
        socket.send(message);
    }
    protected String changeMessage(String serverMessage) throws JsonProcessingException {
        return ServerMessageWrapper.changeMessage(serverMessage);
    }
    protected abstract void action() throws Exception;
}
