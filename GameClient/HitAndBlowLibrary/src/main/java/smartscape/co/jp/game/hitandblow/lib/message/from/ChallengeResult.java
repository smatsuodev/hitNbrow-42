package smartscape.co.jp.game.hitandblow.lib.message.from;

import com.fasterxml.jackson.core.JsonProcessingException;
import smartscape.co.jp.game.hitandblow.lib.message.base.HitAndBlowMessageBase;
import smartscape.co.jp.game.hitandblow.lib.message.body.MessageData;

import java.util.ArrayList;
import java.util.LinkedHashMap;

public class ChallengeResult extends HitAndBlowMessageBase {
    private ActionResult actionResult;
    public ChallengeResult(){

    }
    public ChallengeResult(String stateType, String messageType, Object body){
        super(stateType, messageType, body);
    }

    private ChallengeResult(HitAndBlowMessageBase base) throws JsonProcessingException {
        super(base.state, base.messageType, base.body);
        this.actionResult = ActionResult.readValue( base.body);
    }

    public static ChallengeResult readValue(HitAndBlowMessageBase base) throws JsonProcessingException {
        return new ChallengeResult(base);
    }

    public String getMessage(){
        return this.actionResult.toString();
    }
    public ActionResult getActionResult(){
        return this.actionResult;
    }
}