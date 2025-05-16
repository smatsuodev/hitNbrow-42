package org.smartscape.co.jp;
import org.smartscape.co.jp.player.MyPlayer;

import java.net.URI;
import java.net.URISyntaxException;
import java.text.MessageFormat;

//TIP コードを<b>実行</b>するには、<shortcut actionId="Run"/> を押すか、
// ガターで <icon src="AllIcons.Actions.Execute"/> アイコンをクリックします。
public class Main {
    public static void main(String[] args) throws URISyntaxException, InterruptedException {
        String host = args[0];
        String port = args[1];
        MyPlayer player = new MyPlayer();
        MyWebSocketClient client = new MyWebSocketClient(new URI(MessageFormat.format("ws://{0}:{1}",host, port)),(socket, res) -> {
            player.think(res);
        });
        client.connectBlocking();
        player.setSession(client);
        try {
            client.latch.await();

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}