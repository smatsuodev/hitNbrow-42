@echo off
setlocal


rem ユーザーにJavaのbinディレクトリのパスを入力させる
echo 動作確認しているjdkはtemurin-16.0.2です。
set /p JAVA_BIN_PATH="Please enter the path to the Java16 bin directory: "

rem 入力されたパスを確認
if not exist "%JAVA_BIN_PATH%\java.exe" (
	echo Invalid path. Java executable not found.
	pause
	exit /b 1
)

set PATH=%JAVA_BIN_PATH%;%PATH%
set LIB_DIR=.\package\ai_lib
set MAIN_JAR=.\package\HitAndBlowAIPlayer-1.0.0.jar

java.exe -cp %LIB_DIR%\* -jar %MAIN_JAR% localhost 8088
pause
endlocal