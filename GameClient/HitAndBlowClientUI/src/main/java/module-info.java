module org.smartscape.co.jp.hitandblowclientui {
    requires javafx.controls;
    requires javafx.fxml;

//    requires org.controlsfx.controls;
//    requires com.dlsc.formsfx;
//    requires org.kordamp.bootstrapfx.core;
    requires org.smartscape.co.jp.HitAndBlowLibrary;
    requires org.apache.commons.lang3;
    requires Java.WebSocket;
    requires java.desktop;

    opens org.smartscape.co.jp.hitandblowclientui to javafx.fxml;
    exports org.smartscape.co.jp.hitandblowclientui;
    exports org.smartscape.co.jp.hitandblowclientui.dialog.controller;
    opens org.smartscape.co.jp.hitandblowclientui.dialog.controller to javafx.fxml;
}