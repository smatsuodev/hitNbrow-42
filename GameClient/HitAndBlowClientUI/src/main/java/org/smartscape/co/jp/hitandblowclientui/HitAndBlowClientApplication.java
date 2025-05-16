package org.smartscape.co.jp.hitandblowclientui;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Modality;
import javafx.stage.Stage;
import javafx.stage.StageStyle;
import javax.swing.JOptionPane;

import smartscape.co.jp.game.hitandblow.lib.SocketAccessor;
import smartscape.co.jp.game.hitandblow.lib.message.to.SetName;
import smartscape.co.jp.game.hitandblow.lib.message.ServerMessage;

import java.io.IOException;
import java.net.ConnectException;
import java.net.URI;
import java.net.URISyntaxException;
import java.text.MessageFormat;
import java.util.List;
import java.util.Random;

public class HitAndBlowClientApplication extends Application {
    Stage mainStage;
    Stage modalStage;
    HitAndBlowClientController mainController;
    @Override
    public void start(Stage stage) throws IOException {
        FXMLLoader mainLoader = new FXMLLoader(HitAndBlowClientApplication.class.getResource("HitAndBlowClient.fxml"));
        Scene scene = new Scene(mainLoader.load());
        this.mainController = mainLoader.getController();

        stage.setTitle("Hello!");
        stage.setScene(scene);
        stage.setMinWidth(420);
        stage.setMinHeight(500);
        stage.show();
        stage.setOnCloseRequest(windowEvent -> {
            Platform.exit();
            System.exit(0);
        });
        this.mainStage = stage;

        this.modalStage = new Stage();
        this.modalStage.initModality(Modality.APPLICATION_MODAL);
        this.modalStage.initStyle(StageStyle.UNDECORATED);
//        FXMLLoader modalFxmlLoader = new FXMLLoader(HitAndBlowClientApplication.class.getResource("MatchingWaitDlg.fxml"));
//        Scene modalScene = new Scene(modalFxmlLoader.load());
//        this.modalStage.setScene(modalScene);
        Parameters params = getParameters();
        List<String> args = params.getRaw();
        if (args.size() == 3){
            try {
                SocketAccessor accessor = getSocketAccessor(args);
                if (!accessor.connectBlocking()){
                    throw new ConnectException();
                }else{
                    this.mainController.setSocket(accessor);
                }
            } catch (URISyntaxException e) {
                System.out.println("URIが無効です: " + e.getMessage());
                JOptionPane.showMessageDialog(null, "URIが無効です。", "確認",JOptionPane.ERROR_MESSAGE);
            } catch (ConnectException e) {
                System.out.println("接続に失敗しました: " + e.getMessage());
                JOptionPane.showMessageDialog(null, "接続に失敗しました。", "確認",JOptionPane.ERROR_MESSAGE);
                this.mainStage.close();
            } catch (Exception e) {
                System.out.println("他のエラーが発生しました: " + e.getMessage());
                JOptionPane.showMessageDialog(null, "他のエラーが発生しました。", "確認",JOptionPane.ERROR_MESSAGE);
            }

        }else{
            JOptionPane.showMessageDialog(null, "引数が不足しているため起動に失敗しました。", "確認",JOptionPane.ERROR_MESSAGE);
            this.mainStage.close();
        }
    }

    private SocketAccessor getSocketAccessor(List<String> args) throws IOException, URISyntaxException {
        String host = args.get(0);
        String port = args.get(1);
        String name = args.get(2);
        SocketAccessor accessor = new SocketAccessor(new URI(MessageFormat.format("ws://{0}:{1}",host, port)), (socket, res) -> {
            Platform.runLater(() -> {
                try {
                    if (ServerMessage.SET_NAME.matcher(res).find()) {
                        this.mainController.status = HitAndBlowClientController.StatusType.set_name;
                        this.mainStage.setTitle(name);
                        new SetName(socket, name).start();
                    } else if (ServerMessage.SET_NUMBER.matcher(res).find()) {
                        this.mainController.status = HitAndBlowClientController.StatusType.set_number;
                        this.mainController.showSetMyNumber();
                    }
                    this.mainController.logText.appendText(res + "\n");
                    this.mainController.logText.setScrollTop(Double.MAX_VALUE); // スクロールを最下部に移動
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            });
        });
        return accessor;
    }

    public static void main(String[] args) {
        launch(args);
    }




}