# hit and blow Game Master
## 実行環境
python 3.12

requirements.txtより必要ライブラリをインストールしてください
```
pip install -r requirements.txt
```

## 実行方法
以下コマンドでGameMasterサーバーが起動します

プレイヤークライアントが2つ接続されるとゲームが開始します

デフォルトの待ち受けポートは8088です
```
python .\run.py
```

## オプション
 - --no-timeout: プレイヤークライアントの10秒タイムアウト制限を一時的に無効化します
 - --wait [wait]: プレイヤークライアントの応答後、指定時間待機します
 - -v: デバッグモード(プレイヤークライアント通信ログ、処理結果を表示)
