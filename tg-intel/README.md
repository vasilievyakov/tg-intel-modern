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

2. **Установите зависимости**
```bash
# Backend
pip install -r apps/backend/requirements.txt

# Frontend
pnpm install
```

3. **Настройте переменные окружения**
```bash
cp env.example .env
# Отредактируйте .env файл с вашими настройками
```

4. **Запустите сервисы**
```bash
# Backend (терминал 1)
python start_backend.py

# Frontend (терминал 2)
cd apps/frontend && pnpm dev
```

5. **Откройте приложение**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

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
# Запуск в режиме разработки
make run:dev

# Миграции БД
make migrate

# Деплой
make deploy:backend
make deploy:frontend
```

## Лицензия

MIT
