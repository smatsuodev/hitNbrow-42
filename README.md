# hitNbrow

- documents\interface.md
    - ゲームマスタ、AIプレイヤー間のWebsocket通信スキーマ

- documents\実装範囲\実装範囲_プレイヤー視点.pdf
    - ゲームマスタ、AIプレイヤー間の処理シーケンス

- GameClient
    - GameClient\HitAndBlowClientUI
        - 画面UIでゲームマスタとHitAndBlowを実施できるクライアント。作ったプレイヤーの動作確認時等で利用可
    - GameClient\HitAndBlowAIPlayer
        - JAVAで実装された、プレイヤーのスケルトン。自由に変更等使ってもよい
    - GameClient\package
        - ビルド済みの画面UI、プレイヤーのスケルトン、run.bat、ai_run.batで実行

- GameMaster
    - Pythonで実装された、ゲームマスタ。作ったプレイヤーの動作確認で利用可能
    - GameMaster\README.mdを参照
    - Linux環境などではPythonの仮想環境で実行する、Windowsでは仮想環境でなくてもよい
    - tester\random_tester.html
        - JavaScriptで実装された、プレイヤーのスケルトン。自由に変更等使ってもよい

 - viewer
    - プレイヤー同士の対戦の状況を可視化するビューア。対戦の観戦に使用する
   
- demoAi_ver_0_1
    - Pythonで実装された、プレイヤーのスケルトン。自由に変更等つかってもよい