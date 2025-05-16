package org.smartscape.co.jp.player;
import lombok.Setter;
import org.java_websocket.client.WebSocketClient;
import smartscape.co.jp.game.hitandblow.lib.message.base.HitAndBlowMessageBase;
import smartscape.co.jp.game.hitandblow.lib.message.from.*;
import smartscape.co.jp.game.hitandblow.lib.message.to.*;

import java.io.IOException;
import java.net.http.WebSocket;
import java.util.ArrayList;
import java.util.List;

public class MyPlayer {

    @Setter
    private WebSocketClient session;
    private String mynumber;

    private final List<OpponentActionResult> opponentActionResultList = new ArrayList<>();

    public void think(String inMessage) throws IOException {
        HitAndBlowMessageBase base =  HitAndBlowMessageBase.fromJsonString(inMessage);
        switch (base.messageType) {
            case "requestPlayerName"://プレイヤー名要求
                SetName("山田太郎");
                break;
            case "message":
                break;
            case "roundResult":
                break;
            case "gameResult":
                break;
            case "requestSecretNumber":
                //自分の数値を考える
                this.mynumber = "1234";
                SetNumber(this.mynumber);
                break;
            case "requestItemAction":
                //アイテムを使うのか考える？
                //TODO 暫定で不使用固定
                NotUserItem();
                break;
            case "itemActionResult-pass"://アイテム使用応答結果通知 使用なし
                break;
            case "itemActionResult-target"://アイテム使用応答結果通知 ターゲット
                break;
            case "itemActionResult-high-low"://アイテム使用応答結果通知 ターゲット
                break;
            case "itemActionResult-shuffle"://アイテム使用応答結果通知 ターゲット
                break;
            case "itemActionResult-change"://アイテム使用応答結果通知 ターゲット
                break;
            case "requestChallengeNumber":
                //TODO 相手の番号が何か考えて答える
                CallNumber("9876");
                break;
            case "challengeResult":
                //TODO 相手の番号が何か考えて答えるHIT数、Blow数を受け取る。
                System.out.println(base.toJsonString());
                break;
            case "opponentActionResult"://相手プレイヤーの行動通知
                OpponentActionResult opponentActionResult = OpponentActionResult.readValue(base);
                this.opponentActionResultList.add(opponentActionResult);
                break;
            default:
                break;
        }
    }

    private void CallNumber(String number) throws IOException {
        new CallNumber(this.session, number).start();
    }

    private void ChangeAction(String number) throws IOException {
        new ChangeAction(this.session, number).start();
    }

    private void HiLowAction() throws IOException {
        new HiLowAction(this.session).start();
    }

    private void NotUserItem() throws IOException {
        new NotUserItem(this.session).start();
    }

    private void SetName(String name) throws IOException {
        new SetName(this.session, name).start();
    }
    private void SetNumber(String number) throws IOException {
        new SetNumber(this.session,number).start();;
    }

    private void ShuffleAction(String number) throws IOException {
        new ShuffleAction(this.session, number).start();
    }

    private void TargetAction(String number) throws IOException {
        new TargetAction(this.session, number).start();
    }

}
