# Скрипт для запуска tg-intel приложения (backend + frontend)
# Использование: .\start-app.ps1

$ErrorActionPreference = 'Stop'

# Переходим в корень проекта
$repoRoot = (Get-Item $PSScriptRoot).FullName
Set-Location -Path $repoRoot

Write-Host "🚀 Запуск tg-intel приложения..." -ForegroundColor Green
Write-Host "📁 Рабочая директория: $repoRoot" -ForegroundColor Cyan

# Проверяем наличие виртуального окружения
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "❌ Виртуальное окружение не найдено!" -ForegroundColor Red
    Write-Host "Запустите сначала: make init" -ForegroundColor Yellow
    exit 1
}

# Проверяем зависимости frontend
if (-not (Test-Path "apps\frontend\node_modules")) {
    Write-Host "❌ Зависимости frontend не установлены!" -ForegroundColor Red
    Write-Host "Запустите сначала: make init" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Все зависимости найдены" -ForegroundColor Green

# Функция для запуска backend
function Start-Backend {
    Write-Host "🐍 Запуск backend сервера..." -ForegroundColor Yellow
    Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd '$repoRoot'; .venv\Scripts\activate; python start_backend.py" -WindowStyle Normal
}

# Функция для запуска frontend
function Start-Frontend {
    Write-Host "⚛️ Запуск frontend сервера..." -ForegroundColor Yellow
    Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd '$repoRoot\apps\frontend'; pnpm dev" -WindowStyle Normal
}

# Запускаем оба сервера
Start-Backend
Start-Sleep -Seconds 2
Start-Frontend

Write-Host ""
Write-Host "🎉 Приложение запущено!" -ForegroundColor Green
Write-Host "📱 Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "🔧 Backend: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Для остановки закройте окна терминалов" -ForegroundColor Yellow
