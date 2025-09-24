@echo off
echo 🚀 Запуск tg-intel приложения...
echo.

REM Проверяем наличие виртуального окружения
if not exist ".venv\Scripts\python.exe" (
    echo ❌ Виртуальное окружение не найдено!
    echo Запустите сначала: make init
    pause
    exit /b 1
)

REM Проверяем зависимости frontend
if not exist "apps\frontend\node_modules" (
    echo ❌ Зависимости frontend не установлены!
    echo Запустите сначала: make init
    pause
    exit /b 1
)

echo ✅ Все зависимости найдены
echo.

REM Запускаем backend в новом окне
echo 🐍 Запуск backend сервера...
start "Backend Server" cmd /k ".venv\Scripts\activate.bat && python start_backend.py"

REM Ждем немного
timeout /t 3 /nobreak >nul

REM Запускаем frontend в новом окне
echo ⚛️ Запуск frontend сервера...
start "Frontend Server" cmd /k "cd apps\frontend && pnpm dev"

echo.
echo 🎉 Приложение запущено!
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo.
echo 💡 Для остановки закройте окна терминалов
pause
