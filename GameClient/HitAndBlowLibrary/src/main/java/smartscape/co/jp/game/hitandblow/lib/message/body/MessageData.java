package smartscape.co.jp.game.hitandblow.lib.message.body;

import java.util.LinkedHashMap;


public record MessageData(String message) {

    public static MessageData readValue(Object body) {
        return new MessageData(((LinkedHashMap) body).get("message").toString());
    }

}
