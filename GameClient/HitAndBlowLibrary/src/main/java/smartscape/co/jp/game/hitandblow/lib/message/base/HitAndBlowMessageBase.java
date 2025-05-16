package smartscape.co.jp.game.hitandblow.lib.message.base;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.Data;

@Data
public class HitAndBlowMessageBase{
    public String state;
    public String messageType;
    public Object body;
    public HitAndBlowMessageBase(){

    }
    public HitAndBlowMessageBase(String state, String messageType, Object body){
        this.state = state;
        this.messageType = messageType;
        this.body = body;
    }
    public String toJsonString(){
        ObjectMapper objectMapper = new ObjectMapper();
        try {
            return objectMapper.writeValueAsString(this);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }

    public static HitAndBlowMessageBase fromJsonString(String jsonString) {
        ObjectMapper objectMapper = new ObjectMapper();

        try {
            return objectMapper.readValue(jsonString, HitAndBlowMessageBase.class);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
    }
}
