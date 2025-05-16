package smartscape.co.jp.game.hitandblow.lib.message.from;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.Getter;
import smartscape.co.jp.game.hitandblow.lib.message.base.HitAndBlowMessageBase;
import smartscape.co.jp.game.hitandblow.lib.message.body.MessageData;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;


public class OpponentActionResult  extends HitAndBlowMessageBase {
    private List<ActionResult> actionResults;
    public OpponentActionResult(String stateType, String messageType, Object body){
        super(stateType, messageType, body);
    }

    private OpponentActionResult(HitAndBlowMessageBase base) throws JsonProcessingException {
        super(base.state, base.messageType, base.body);
        this.actionResults = new ArrayList<>();
        LinkedHashMap linkedHashMap= ((LinkedHashMap) body);
        ArrayList<Object> array = (ArrayList<Object>) linkedHashMap.get("actionResults");
        for (Object body : array){
            this.actionResults.add(ActionResult.readValue(body));
        }
    }

    public static OpponentActionResult readValue(HitAndBlowMessageBase base) throws JsonProcessingException {
        return new OpponentActionResult(base);
    }

    public String getActionResults(){
        StringBuilder result = new StringBuilder();
        for(ActionResult actionResult : this.actionResults){
            result.append(actionResult.getResultStr());
            result.append("\n");
        }
        return result.toString();
    }
}
