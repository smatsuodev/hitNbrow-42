#!/bin/bash
echo "動作確認しているjdkはtemurin-16.0.2です。"
read -p "Please enter the path to the Java16 bin directory: " JAVA_BIN_PATH

if [ ! -f "$JAVA_BIN_PATH/java" ]; then
    echo "Invalid path. Java executable not found."
    exit 1
fi

export PATH="$JAVA_BIN_PATH:$PATH"
LIB_DIR="./package/lib"
MAIN_JAR="./package/HitAndBlowClientUI-1.0.0.jar"

java --module-path $LIB_DIR --add-modules javafx.controls,javafx.fxml -cp $LIB_DIR/* -jar $MAIN_JAR localhost 8088 NIプレイヤー
