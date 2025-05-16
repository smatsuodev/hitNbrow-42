package smartscape.co.jp.game.hitandblow.lib.message;

public class ClientMessage {
    public static final String SET = "{\"state\":\"start_game\",\"messageType\":\"requestSecretNumber\",\"body\":{\"number\":\"%s\"}}";
    public static final String CALL = "{\"messageType\":\"requestChallengeNumber\",\"body\":{\"action\":\"call\",\"number\":\"%s\"}}";
    public static final String TARGET = "{\"messageType\":\"requestItemAction-target\",\"body\":{\"action\":\"target\",\"number\":\"%s\"}}";
    public static final String HIGH_AND_LOW = "{\"messageType\":\"requestItemAction-high-low\",\"body\":{\"action\":\"high-low\"}}";
    public static final String SHUFFLE = "{\"messageType\":\"requestItemAction-shuffle\",\"body\":{\"action\":\"shuffle\",\"number\":\"%s\"}}";
    public static final String CHANGE = "{\"messageType\":\"requestItemAction-change\",\"body\":{\"action\":\"change\",\"number\":\"%s\"}}";
    public static final String SET_NAME = "{\"messageType\":\"requestPlayerName\",\"body\":{\"playerName\":\"%s\"}}";
    public static final String NOT_USE_ITEM = "{\"messageType\":\"requestItemAction-pass\",\"body\":{\"action\":\"pass\"}}";
}
