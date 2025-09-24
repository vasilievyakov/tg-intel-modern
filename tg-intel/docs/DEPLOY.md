# Деплой tg-intel

## Обзор

Проект состоит из двух частей:
- **Backend** (FastAPI) - деплоится на Railway
- **Frontend** (Next.js) - деплоится на Vercel
- **База данных** - Supabase PostgreSQL

## Предварительные требования

1. Аккаунты на:
   - [Railway](https://railway.app) (backend)
   - [Vercel](https://vercel.com) (frontend)
   - [Supabase](https://supabase.com) (база данных)

2. Telegram API credentials:
   - Получить API ID и API Hash на https://my.telegram.org

## Шаг 1: Настройка базы данных (Supabase)

1. Создайте новый проект в Supabase
2. Перейдите в SQL Editor
3. Выполните SQL из `infra/sql/schema.sql`
4. Сохраните:
   - Database URL
   - Service Role Key
   - Project URL

## Шаг 2: Деплой Backend (Railway)

1. Подключите GitHub репозиторий к Railway
2. Создайте новый сервис из репозитория
3. Установите переменные окружения:

```bash
# Database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_DB_URL=postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres

# Telegram
TG_API_ID=your_telegram_api_id
TG_API_HASH=your_telegram_api_hash

# Backend
BACKEND_PORT=8000
CRON_FETCH_MINUTES=5

# CORS (будет настроен после деплоя frontend)
CORS_ORIGINS=https://your-frontend-domain.vercel.app
CORS_ALLOW_CREDENTIALS=true
```

4. Railway автоматически определит Dockerfile и запустит сервис
5. Сохраните URL backend сервиса

## Шаг 3: Деплой Frontend (Vercel)

1. Подключите GitHub репозиторий к Vercel
2. Установите корневую директорию: `apps/frontend`
3. Установите переменные окружения:

```bash
NEXT_PUBLIC_API_BASE=https://your-backend-url.railway.app
```

4. Vercel автоматически определит Next.js и запустит сборку
5. Сохраните URL frontend сервиса

## Шаг 4: Настройка CORS

После деплоя frontend обновите переменную `CORS_ORIGINS` в Railway:

```bash
CORS_ORIGINS=https://your-frontend-domain.vercel.app
```

## Проверка деплоя

1. **Backend**: `https://your-backend-url.railway.app/healthz`
2. **Frontend**: `https://your-frontend-domain.vercel.app`
3. **API Docs**: `https://your-backend-url.railway.app/docs`

## Локальная разработка

```bash
# Backend
cd apps/backend
python -m venv .venv
.venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload

# Frontend
cd apps/frontend
pnpm install
pnpm dev
```

## Мониторинг

- **Railway**: Логи и метрики в дашборде Railway
- **Vercel**: Логи и аналитика в дашборде Vercel
- **Supabase**: Мониторинг БД в дашборде Supabase

## Troubleshooting

### SSL ошибки на Windows
Если возникают SSL ошибки при локальной разработке:
```bash
set PYTHONHTTPSVERIFY=0
```

### Проблемы с Telegram API
- Убедитесь, что API ID и Hash корректны
- Проверьте, что сессия создается в `.secrets/telethon.session`
- При необходимости используйте прокси: `TG_PROXY_URL=socks5://user:pass@host:port`
