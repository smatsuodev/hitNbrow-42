package smartscape.co.jp.game.hitandblow.lib;

import com.fasterxml.jackson.core.JsonProcessingException;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;
import smartscape.co.jp.game.hitandblow.lib.message.to.common.ServerMessageWrapper;

import java.io.*;
import java.net.URI;

public class SocketAccessor extends WebSocketClient{
    public interface Callback {
        void onComplete(WebSocketClient socket , String message);
    }
    private final Callback callback;
    public SocketAccessor(URI serverUri, Callback callback) throws IOException {
        super(serverUri);
        this.callback = callback;
    }


    @Override
    public void onOpen(ServerHandshake serverHandshake) {

        System.out.println("Connected to server");
    }

    @Override
    public void onMessage(String message) {
        System.out.println("Received message: " + message);
        if(this.callback != null){

            String serverMessage = null;
            try {
                serverMessage = changeMessage(message);
            } catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }
            this.callback.onComplete((WebSocketClient)this, serverMessage);
        }
    }


    @Override
    public void onClose(int code, String reason, boolean remote) {
        System.out.println("Disconnected from server");
    }

    @Override
    public void onError(Exception ex) {
        System.out.println("エラー: " + ex.getMessage());
    }

    private String changeMessage(String serverMessage) throws JsonProcessingException {
        return ServerMessageWrapper.changeMessage(serverMessage);
    }
}
