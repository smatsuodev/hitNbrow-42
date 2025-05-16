package smartscape.co.jp.game.hitandblow.lib.message.from;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.Data;
import smartscape.co.jp.game.hitandblow.lib.message.base.HitAndBlowMessageBase;
import smartscape.co.jp.game.hitandblow.lib.message.body.MessageData;

@Data
public class RequestSecretNumberReq extends HitAndBlowMessageBase {
    private MessageData messageClass;
    public RequestSecretNumberReq(String stateType, String messageType, Object body){
        super(stateType, messageType, body);
    }


    private RequestSecretNumberReq(HitAndBlowMessageBase base) throws JsonProcessingException {
        super(base.state, base.messageType, base.body);
        ObjectMapper objectMapper = new ObjectMapper();
        this.messageClass = MessageData.readValue(base.body);
    }

    public static RequestSecretNumberReq readValue(HitAndBlowMessageBase base) throws JsonProcessingException {
        return new RequestSecretNumberReq(base);
    }

    public String getMessage(){
        return this.messageClass.message();
    }
}
