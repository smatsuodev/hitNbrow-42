package smartscape.co.jp.game.hitandblow.lib.message.to.common;

import com.fasterxml.jackson.core.JsonProcessingException;

import java.text.MessageFormat;

import smartscape.co.jp.game.hitandblow.lib.message.base.HitAndBlowMessageBase;
import smartscape.co.jp.game.hitandblow.lib.message.from.*;

public class ServerMessageWrapper {
//    public static final Pattern START = Pattern.compile("\\{\"state\":\"connect\",\"messageType\":\"requestPlayerName\",\"body\":\\{\"message\":\"Please declare your player name.\"}}");
//    public static final Pattern SET_NUMBER = Pattern.compile("\\{\"state\":\"start_game\",\"messageType\":\"requestSecretNumber\",\"body\":\\{\"message\":\"Please declare the secret number\"}}");
//    public static final Pattern CALL_OR_ITEM = Pattern.compile("コールまたはアイテムの使用を宣言してください。");
//    public static final Pattern DEF_ITEM = Pattern.compile("アイテムの使用する場合は使用を宣言してください。使用しない場合はNOを指定してください。");
//
//
//    //↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓アイテム仕様関連↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
//    public static final Pattern ATTACK_TARGET = Pattern.compile("相手がアイテムTARGETを使用しました。指定された値は([0-9])です");
//    public static final Pattern ATTACK_HIGH_AND_LOW = Pattern.compile("相手がアイテムHIGH＆LOWを使用しました。");
//    public static final Pattern ATTACK_SHUFFLE = Pattern.compile("相手がアイテムSHUFFLEを使用しました。");
//    public static final Pattern ATTACK_CHANGE = Pattern.compile("相手がアイテムCHANGEを使用しました。");
//
//    //↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓動作依頼に対するレスポンス↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
//    public static final Pattern USE_CALL_SUCCESS = Pattern.compile("あなたがCALLを使用した結果Hit\\([0-4]\\)Blow\\([0-4]\\)でした。");
//    public static final Pattern USE_ITEM_ERROR = Pattern.compile("相手がこのラウンドでアイテムを使用済みのため、あなたのアイテムは使用できません。");
//    public static final Pattern USE_TARGET_SUCCESS = Pattern.compile("あなたがTARGETを使用した結果(([1-4]桁目にヒットしました。)|(値はありませんでした。))");
//    public static final Pattern USE_HIGH_AND_LOW_SUCCESS = Pattern.compile("あなたがHIGH_AND_LOWを使用した結果H\\([0-4]\\)L\\([0-4]\\)でした。");
//    public static final Pattern USE_SHUFFLE_SUCCESS = Pattern.compile("あなたはSHUFFLEを使用しました。");
//    public static final Pattern USE_CHANGE_SUCCESS = Pattern.compile("あなたはCHANGEを使用しました。");
//
//    //↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓勝敗決定関連↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
//    public static final Pattern WIN_1 = Pattern.compile("相手がルール違反をしました。あなたの勝ちです。");
//    public static final Pattern WIN_2 = Pattern.compile("相手の数値を言い当てました。あなたの勝ちです。");
//    public static final Pattern LOSS_1 = Pattern.compile("ルール違反\\(((HIGH_AND_LOW)|(TARGET)|(SHUFFLE)|(CHANGE)|(値指定))\\)です、あなたの負けです。");
//    public static final Pattern LOSS_2 = Pattern.compile("相手に数値を言い当てられました。あなたの負けです。");
//    public static final Pattern DRAW = Pattern.compile("引き分けです。ゲームを終了します。");

    public static String changeMessage(String serverMessage) throws IllegalArgumentException, JsonProcessingException {

        HitAndBlowMessageBase base =  HitAndBlowMessageBase.fromJsonString(serverMessage);
        String result = "";
        try {
            switch (base.messageType) {
                case "requestPlayerName"://プレイヤー名要求
                    RequestPlayerNameReq playerNameReq = RequestPlayerNameReq.readValue(base);
                    result = CHANGE_START(playerNameReq.getMessage());
                    break;
                case "message":
                case "roundResult":
                case "gameResult":
                    result = serverMessage;
                    break;
                case "requestSecretNumber"://初期数値設定要求
                    RequestSecretNumberReq secretNumberReq = RequestSecretNumberReq.readValue(base);
                    result = CHANGE_SET_NUMBER(secretNumberReq.getMessage());
                    break;
                case "requestItemAction"://アイテム使用要求
                    result = CHANGE_USE_ITEM(serverMessage);
                    break;
                case "itemActionResult-pass"://アイテム使用応答結果通知 使用なし
                case "itemActionResult-target"://アイテム使用応答結果通知 ターゲット
                case "itemActionResult-high-low"://アイテム使用応答結果通知 ターゲット
                case "itemActionResult-shuffle"://アイテム使用応答結果通知 ターゲット
                case "itemActionResult-change"://アイテム使用応答結果通知 ターゲット
                    ActionResult itemActionResult = ActionResult.readValue(base.body);
                    result = CHANGE_ITEM_ACTION_RESULT(itemActionResult.getResultStr());
                    break;
                case "requestChallengeNumber":
                    result = CHANGE_REQUEST_CHALLENGE_NUMBER(serverMessage);
                    break;
                case "challengeResult":
                    ChallengeResult challengeResult = ChallengeResult.readValue(base);
                    result = CHANGE_CHALLENGE_RESULT(challengeResult.getActionResult().getResultStr());
                    break;
                case "opponentActionResult":
                    OpponentActionResult opponentActionResult = OpponentActionResult.readValue(base);
                    result = CHANGE_OPPONENT_ACTION_RESULT(opponentActionResult.getActionResults());
                    break;
                default:
                    result = serverMessage;
                    break;
            }
        }catch (IllegalArgumentException e){
            result = MessageFormat.format("想定しないメッセージ\n{0}", serverMessage);
        }
        return result;
    }

    private static String CHANGE_DRAW(String serverMessage) {
        return serverMessage;
    }

    private static String CHANGE_LOSS_2(String serverMessage) {
        return serverMessage;
    }

    private static String CHANGE_LOSS_1(String serverMessage) {
        return serverMessage;
    }

    private static String CHANGE_WIN_2(String serverMessage) {
        return serverMessage;
    }

    private static String CHANGE_WIN_1(String serverMessage) {
        return serverMessage;
    }

    private static String CHANGE_USE_CHANGE_SUCCESS(String serverMessage) {
        return serverMessage;
    }

    private static String CHANGE_USE_SHUFFLE_SUCCESS(String serverMessage) {
        return serverMessage;
    }

    private static String CHANGE_USE_HIGH_AND_LOW_SUCCESS(String serverMessage) {
        return serverMessage;
    }

    private static String CHANGE_USE_TARGET_SUCCESS(String serverMessage) {
        return serverMessage;
    }

    private static String CHANGE_USE_ITEM_ERROR(String serverMessage) {
        return serverMessage;
    }

    private static String CHANGE_USE_CALL_SUCCESS(String serverMessage) {
        return serverMessage;
    }

    private static String CHANGE_ATTACK_CHANGE(String serverMessage) {
        return serverMessage;
    }

    private static String CHANGE_ATTACK_SHUFFLE(String serverMessage) {
        return serverMessage;
    }

    private static String CHANGE_ATTACK_HIGH_AND_LOW(String serverMessage) {
        return serverMessage;
    }

    private static String CHANGE_ATTACK_TARGET(String serverMessage) {
        return serverMessage;
    }

    private static String CHANGE_DEF_ITEM(String serverMessage) {
        return serverMessage;
    }


    private static String CHANGE_START(String serverMessage) {
        return "プレイヤー名を指定してください。（起動パラメータで指定されています）";
    }
    private static String CHANGE_SET_NUMBER(String serverMessage) {
        return "0~9で４桁の数値を指定してください。数値を当てられると負けとなります。";
    }
    private static String CHANGE_OPPONENT_ACTION_RESULT(String serverMessage){
        return MessageFormat.format("相手プレイヤーが実施したアクションです。\n{0}",serverMessage);
    }
    private static String CHANGE_ITEM_ACTION_RESULT(String serverMessage){
        return MessageFormat.format("アクション実施結果です。\n{0}",serverMessage);
    }

    private static String CHANGE_USE_ITEM(String serverMessage) {
        return "アイテムを使用する場合は宣言してください。使用しない場合は「使用なし」を指定してください。";
    }

    private static String CHANGE_CHALLENGE_RESULT(String serverMessage) {
        return MessageFormat.format("CALLの結果です。\n{0}",serverMessage);
    }

    private static String CHANGE_REQUEST_CHALLENGE_NUMBER(String serverMessage) {
        return "予想する4桁の数値をCALLしてください。";
    }

}
