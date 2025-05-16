module org.smartscape.co.jp.HitAndBlowLibrary {
    requires org.apache.commons.lang3;
    requires Java.WebSocket;
    requires com.fasterxml.jackson.databind;
    requires static lombok;
    exports smartscape.co.jp.game.hitandblow.lib;
    exports smartscape.co.jp.game.hitandblow.lib.message;
    exports smartscape.co.jp.game.hitandblow.lib.net;
    exports smartscape.co.jp.game.hitandblow.lib.message.to;
    exports smartscape.co.jp.game.hitandblow.lib.message.to.common;
    exports smartscape.co.jp.game.hitandblow.lib.message.base;
    exports smartscape.co.jp.game.hitandblow.lib.message.body;
    exports smartscape.co.jp.game.hitandblow.lib.message.from;
    opens smartscape.co.jp.game.hitandblow.lib.message.from to com.fasterxml.jackson.databind;
}