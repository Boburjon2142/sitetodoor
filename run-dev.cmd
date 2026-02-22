@echo off
setlocal
set ROOT=%~dp0

echo Starting backend and frontend...

start "SITE-TO-DOOR Backend" cmd /k "cd /d %ROOT%backend && set USE_SQLITE=1 && python manage.py migrate && python manage.py seed_demo_users && python manage.py seed_catalog && python manage.py runserver 127.0.0.1:8000"

start "SITE-TO-DOOR Frontend" cmd /k "cd /d %ROOT%frontend && set NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000/api/v1 && npm run dev"

echo.
echo Backend:  http://127.0.0.1:8000/api/docs/
echo Frontend: http://127.0.0.1:3000
echo.
echo Keep both opened terminals running.
endlocal
