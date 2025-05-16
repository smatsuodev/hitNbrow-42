package smartscape.co.jp.game.hitandblow.lib.message.from;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.Data;
import lombok.EqualsAndHashCode;
import smartscape.co.jp.game.hitandblow.lib.message.base.HitAndBlowMessageBase;
import smartscape.co.jp.game.hitandblow.lib.message.body.MessageData;

@EqualsAndHashCode(callSuper = true)
@Data
public final class RequestPlayerNameReq extends HitAndBlowMessageBase {
    private MessageData messageData;
    public RequestPlayerNameReq(){

    }
    public RequestPlayerNameReq(String stateType, String messageType, Object body){
        super(stateType, messageType, body);
    }

    private RequestPlayerNameReq(HitAndBlowMessageBase base) throws JsonProcessingException {
        super(base.state, base.messageType, base.body);
        this.messageData = MessageData.readValue(base.body);
    }

    public static RequestPlayerNameReq readValue(HitAndBlowMessageBase base) throws JsonProcessingException {
        return new RequestPlayerNameReq(base);
    }

    public String getMessage(){
        return this.messageData.message();
    }
}