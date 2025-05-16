@echo off
setlocal


rem ���[�U�[��Java��bin�f�B���N�g���̃p�X����͂�����
echo ����m�F���Ă���jdk��temurin-16.0.2�ł��B
set /p JAVA_BIN_PATH="Please enter the path to the Java16 bin directory: "

rem ���͂��ꂽ�p�X���m�F
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