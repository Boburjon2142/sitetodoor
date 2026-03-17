@echo off
setlocal

powershell -ExecutionPolicy Bypass -File "%~dp0scripts\stop-python-html.ps1"
endlocal
