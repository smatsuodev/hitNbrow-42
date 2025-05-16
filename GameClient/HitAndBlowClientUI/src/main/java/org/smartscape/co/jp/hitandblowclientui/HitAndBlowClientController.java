package org.smartscape.co.jp.hitandblowclientui;

import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.stage.Stage;
import org.java_websocket.client.WebSocketClient;
import org.smartscape.co.jp.hitandblowclientui.dialog.controller.SetNumberDlgController;
import smartscape.co.jp.game.hitandblow.lib.message.to.*;

import java.io.IOException;
import java.text.MessageFormat;

public class HitAndBlowClientController {
    @FXML
    public TextArea logText;
    @FXML
    private Label myNumber;
    @FXML
    private TextField number1;


    private WebSocketClient socket;

    public enum StatusType {
        none,
        set_name,
        set_number
    }
    public StatusType status = StatusType.none;
    @FXML
    protected void onTargetBtn() throws IOException {
        if (this.socket == null){
            this.logText.appendText("serverへ接続していません。\n");
        }
        new TargetAction(this.socket, MessageFormat.format("{0}",this.number1.getText())).start();
    }
    @FXML
    protected void onHiLowBtn() throws IOException {
        if (this.socket == null){
            this.logText.appendText("serverへ接続していません。\n");
        }
        new HiLowAction(this.socket).start();

    }
    @FXML
    protected void onShuffleBtn() throws IOException {
        if (this.socket == null){
            this.logText.appendText("serverへ接続していません。\n");
        }
        this.myNumber.setText(this.number1.getText());
        new ShuffleAction(this.socket, MessageFormat.format("{0}",this.number1.getText())).start();
    }

    @FXML
    protected void onChangeBtn() throws IOException {

        if (this.socket == null){
            this.logText.appendText("serverへ接続していません。\n");
        }
        this.myNumber.setText(this.number1.getText());
        new ChangeAction(this.socket, MessageFormat.format("{0}",this.number1.getText())).start();
    }

    @FXML
    protected void onCallButtonClick() throws IOException {
        if (this.socket == null){
            this.logText.appendText("serverへ接続していません。\n");
        }
        new CallNumber(this.socket, MessageFormat.format("{0}",this.number1.getText())).start();
    }
    @FXML
    protected void onNotUseItemBtn() throws IOException {
        if (this.socket == null){
            this.logText.appendText("serverへ接続していません。\n");
        }else{
            new NotUserItem(this.socket).start();
        }
    }

    public void showSetMyNumber() throws IOException {
        if (this.socket == null && this.status == StatusType.set_number){
            throw new IOException("サーバと接続されていません");
        }
        FXMLLoader fxmlLoader = new FXMLLoader(getClass().getResource("SetNumberDlg.fxml"));
        Parent root = fxmlLoader.load();
        SetNumberDlgController controller = fxmlLoader.getController();

        Platform.runLater(() -> {
            Stage stage = new Stage();
            stage.setTitle("New Window");
            stage.setScene(new Scene(root));
            stage.showAndWait();
            this.myNumber.setText(controller.getNewNumber());
            try {
                new SetNumber(socket, this.getMyNumber()).start();
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        });
    }

    public void setMyNumber(String myNumber) {
        this.myNumber.setText(myNumber);
    }
    public String getMyNumber(){
        return this.myNumber.getText();
    }

    public void setSocket(WebSocketClient socket) {
        this.socket = socket;
    }
}