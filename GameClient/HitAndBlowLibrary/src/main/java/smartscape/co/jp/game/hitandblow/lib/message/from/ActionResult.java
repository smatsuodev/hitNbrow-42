package smartscape.co.jp.game.hitandblow.lib.message.from;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.PropertyAccessor;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import lombok.Getter;
import smartscape.co.jp.game.hitandblow.lib.message.body.MessageData;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;

public class ActionResult {
    String action;
    String playerNumber;
    Object result;

    private ActionResult(String action, String playerNumber, Object result){
        this.action = action;
        this.playerNumber = playerNumber;
        this.result = result;
    }

    public static ActionResult readValue(Object body) {
        String action = ((LinkedHashMap) body).get("action").toString();
        String playerNumber = ((LinkedHashMap) body).get("playerNumber").toString();
        Object result = ((LinkedHashMap) body).get("result");

        return new ActionResult(action, playerNumber, result);
    }

    @JsonIgnore
    public String getResultStr(){
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.setVisibility(PropertyAccessor.FIELD, JsonAutoDetect.Visibility.ANY);
        objectMapper.configure(SerializationFeature.FAIL_ON_EMPTY_BEANS, false);

        try {
            return objectMapper.writeValueAsString(this);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }
}
