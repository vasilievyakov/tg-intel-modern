# tg-intel

Telegram Intelligence Platform - система для мониторинга и анализа Telegram каналов.

## Возможности

- 📊 Мониторинг Telegram каналов
- 🔍 Полнотекстовый поиск по постам
- 🤖 AI-саммаризация контента
- 📱 Современный веб-интерфейс
- ⚡ Реальное время обновлений

## Архитектура

- **Backend**: FastAPI + Telethon + APScheduler
- **Frontend**: Next.js + TypeScript + Tailwind CSS
- **База данных**: Supabase PostgreSQL
- **Деплой**: Railway (backend) + Vercel (frontend)

## Быстрый старт

### Локальная разработка

1. **Клонируйте репозиторий**
```bash
git clone <repository-url>
cd tg-intel
```

2. **Скопируйте и заполните `.env`**
```bash
cp env.example .env
# Укажите SUPABASE_URL, SUPABASE_DB_URL, TG_API_ID, TG_API_HASH и др.
```

3. **Установите зависимости**
```bash
# Backend
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r apps/backend/requirements.txt

# Frontend
corepack enable
pnpm -C apps/frontend install
```

4. **Запустите сервисы**
```bash
# Backend (терминал 1)
python start_backend.py

# Frontend (терминал 2)
pnpm -C apps/frontend dev
```

5. **Проверьте сервисы**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Windows быстрый старт
- `start-app.ps1` или `start-app.bat` — откроют два окна с backend и frontend
- `python simple_server.py` — облегчённый backend без БД (для UI-просмотра)

### Деплой в продакшн

См. подробные инструкции в [docs/DEPLOY.md](docs/DEPLOY.md)

### Деплой в продакшн

См. подробные инструкции в [docs/DEPLOY.md](docs/DEPLOY.md)

## API

Основные эндпоинты:

- `GET /healthz` - проверка здоровья
- `POST /api/channels` - добавление канала
- `GET /api/channels` - список каналов
- `GET /api/channels/{id}/posts` - посты канала
- `POST /api/posts/{id}/summarize` - саммаризация поста

Полная документация: [docs/API.md](docs/API.md)

## Разработка

### Структура проекта

```
tg-intel/
├── apps/
│   ├── backend/          # FastAPI приложение
│   │   ├── api/         # API роутеры
│   │   ├── core/        # Конфигурация и БД
│   │   ├── services/    # Бизнес-логика
│   │   └── models/      # Модели данных
│   └── frontend/        # Next.js приложение
├── docs/                # Документация
├── infra/              # Инфраструктура
└── scripts/            # Скрипты
```

### Полезные команды

```bash
make init             # Создать venv, установить зависимости
make run:backend      # uvicorn backend --reload
make run:frontend     # Next.js dev сервер
make migrate          # Применить миграции (см. infra/sql/schema.sql)
make deploy:backend   # Подсказки по деплою на Railway
make deploy:frontend  # Подсказки по деплою на Vercel
```

## Лицензия

MIT
