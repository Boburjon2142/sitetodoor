@echo off
setlocal
set ROOT=%~dp0

powershell -ExecutionPolicy Bypass -File "%ROOT%scripts\start-python-html.ps1"
