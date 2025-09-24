@echo off
echo Starting tg-intel application...

REM Start backend
echo Starting backend...
start "Backend" cmd /k "cd /d C:\Users\Vasiliev\SCANNER\tg-intel && .venv\Scripts\activate.bat && python start_backend.py"

REM Wait a bit
timeout /t 3 /nobreak >nul

REM Start frontend  
echo Starting frontend...
start "Frontend" cmd /k "cd /d C:\Users\Vasiliev\SCANNER\tg-intel\apps\frontend && pnpm dev"

echo.
echo Application started!
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
pause
