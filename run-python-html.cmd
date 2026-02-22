@echo off
setlocal
set ROOT=%~dp0

cd /d %ROOT%python_html_app
if not exist .venv (
  python -m venv .venv
)

.venv\Scripts\python -m pip install -r requirements.txt
echo.
echo Running on: http://127.0.0.1:5050
echo Do not close this window while using the site.
echo.
.venv\Scripts\python app.py
