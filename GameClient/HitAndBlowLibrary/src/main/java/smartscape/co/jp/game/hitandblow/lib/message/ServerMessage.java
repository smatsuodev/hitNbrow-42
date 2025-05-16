package smartscape.co.jp.game.hitandblow.lib.message;

import java.util.concurrent.LinkedBlockingQueue;
import java.util.regex.Pattern;

public class ServerMessage {
    private ServerMessage(){}

    //↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓動作依頼関連↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
    public static final Pattern SET_NAME = Pattern.compile("プレイヤー名を指定してください");
    public static final Pattern SET_NUMBER = Pattern.compile("0~9で４桁の数値を指定してください。数値を当てられると負けとなります");
    public static final Pattern OPPONENT_ACTION_RESULT = Pattern.compile("相手プレイヤーが実施したアクションです。*");

    //↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓アイテム仕様関連↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
}
