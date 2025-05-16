package org.smartscape.co.jp.hitandblowclientui.dialog.controller;

import javafx.event.ActionEvent;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.stage.Stage;
import javafx.stage.WindowEvent;

public class SetNumberDlgController {
    public TextField number1;
    public TextField number2;
    public TextField number3;
    public TextField number4;
    public Button sendBtn;

    public String getNewNumber(){
        return number1.getText()+number2.getText()+number3.getText()+number4.getText();
    }

    public void OnClickSendBtn(ActionEvent actionEvent) {
        Stage stage = (Stage) sendBtn.getScene().getWindow();
        stage.fireEvent(new WindowEvent(stage, WindowEvent.WINDOW_CLOSE_REQUEST));
    }
}
