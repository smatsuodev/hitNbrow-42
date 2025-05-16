package smartscape.co.jp.game.hitandblow.lib.message.from;

import com.fasterxml.jackson.core.JsonProcessingException;
import smartscape.co.jp.game.hitandblow.lib.message.base.HitAndBlowMessageBase;
import smartscape.co.jp.game.hitandblow.lib.message.body.MessageData;

public class RequestChallengeNumber extends HitAndBlowMessageBase {
    private MessageData messageData;
    public RequestChallengeNumber(){

    }
    public RequestChallengeNumber(String stateType, String messageType, Object body){
        super(stateType, messageType, body);
    }

    private RequestChallengeNumber(HitAndBlowMessageBase base) throws JsonProcessingException {
        super(base.state, base.messageType, base.body);
        this.messageData = MessageData.readValue(base.body);
    }

    public static RequestChallengeNumber readValue(HitAndBlowMessageBase base) throws JsonProcessingException {
        return new RequestChallengeNumber(base);
    }

    public String getMessage(){
        return this.messageData.message();
    }
}