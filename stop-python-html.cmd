@echo off
setlocal

for /f "tokens=5" %%p in ('netstat -ano ^| findstr :5050 ^| findstr LISTENING') do (
  taskkill /PID %%p /F >nul 2>nul
)

echo Stopped app on port 5050 (if running).
endlocal
