@echo off
REM start_appium.bat
REM 启动 Appium Server

echo Starting Appium Server...

if "%1"=="" (
    set PORT=4723
) else (
    set PORT=%1
)

echo Port: %PORT%

appium --address 127.0.0.1 --port %PORT% --log "logs/appium_%PORT%.log" --log-level debug

pause