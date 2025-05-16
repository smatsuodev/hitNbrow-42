package org.smartscape.co.jp;

import org.java_websocket.client.WebSocketClient;
import org.java_websocket.handshake.ServerHandshake;

import java.io.IOException;
import java.net.URI;
import java.util.concurrent.CountDownLatch;

public class MyWebSocketClient extends WebSocketClient {
    public CountDownLatch latch;
    public interface Callback {
        void onMessage(WebSocketClient socket , String message) throws IOException;
    }
    private final Callback callback;

    public MyWebSocketClient(URI serverUri, Callback onMessage) {
        super(serverUri);
        this.callback = onMessage;
        this.latch = new CountDownLatch(1);
    }

    @Override
    public void onOpen(ServerHandshake serverHandshake) {
        System.out.println("Connected to server");
    }

    @Override
    public void onMessage(String s) {
        try {
            System.out.println("onMessage\n" + s );
            this.callback.onMessage(this, s);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public void onClose(int i, String s, boolean b) {

        System.out.println("closed to server");
    }

    @Override
    public void onError(Exception e) {
        System.out.println("error to server");
    }
}
