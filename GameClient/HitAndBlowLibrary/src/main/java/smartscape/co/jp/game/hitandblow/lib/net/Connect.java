package smartscape.co.jp.game.hitandblow.lib.net;

public enum Connect {
    SUCCESS("成功",1),
    FAIL("失敗",2);

    public final String label;
    public final int id;

    private Connect(String label, int id) {	//コンストラクタはprivateで宣言
        this.label = label;
        this.id = id;
    }

    public int getId() {
        return id;
    }
    public String getLabel(){
        return label;
    }
}
