# 📱 tg-intel

Современная система мониторинга и анализа Telegram каналов с продвинутыми таблицами и фильтрацией.

## 🚀 Как запустить

**Предварительные требования**
- Python 3.10+
- Node.js 18+ (вместе с Corepack для pnpm)
- Учетная запись Supabase и Telegram API (см. `env.example`)

**1. Клонируйте репозиторий**
```bash
git clone https://github.com/yourusername/tg-intel.git
cd tg-intel
```

**2. Создайте и заполните `.env`**
```bash
cp env.example .env
# Обновите значения SUPABASE_*, TG_API_* и прочие переменные
```

**3. Установите зависимости**
- Быстрее всего через `make` (macOS/Linux или Windows с Make):
  ```bash
  make init
  ```
- Либо вручную:
  ```bash
  python -m venv .venv
  # macOS/Linux
  source .venv/bin/activate
  # Windows PowerShell
  .venv\Scripts\Activate.ps1

  pip install -r apps/backend/requirements.txt
  corepack enable
  pnpm -C apps/frontend install
  ```

**4. Запустите сервисы**
- Windows: `./start-app.ps1` (PowerShell) или `start-app.bat`
- macOS/Linux: в отдельных терминалах
  ```bash
  # Терминал 1
  .venv/bin/python start_backend.py

  # Терминал 2
  pnpm -C apps/frontend dev
  ```

Frontend откроется на `http://localhost:3000`, backend API — `http://localhost:8000`, Swagger UI — `http://localhost:8000/docs`.

> 💡 Для быстрого теста без базы можно запустить `python simple_server.py`, однако функциональность будет ограничена (нет загрузки каналов в БД).

## ✨ Особенности

- 🔍 **Продвинутый поиск и фильтрация** — глобальный поиск и фильтры для каждой колонки
- 📊 **Современные таблицы** — сортировка, пагинация, адаптивный UI
- 📈 **Аналитика активности** — просмотры, пересылки, ответы, реакции
- 🤖 **AI-саммаризация** — автоматические выжимки по постам
- 🔄 **Автообновления** — регулярный сбор данных через планировщик

## 🧱 Архитектура и технологии

### Backend
- **Python + FastAPI**
- **Telethon** для работы с Telegram API
- **APScheduler** для фоновых задач
- **Supabase PostgreSQL** как основная БД

### Frontend
- **Next.js 15 + React 19 + TypeScript**
- **Tailwind CSS** и **shadcn/ui**
- **TanStack Table** для таблиц

## 📁 Структура проекта
```
tg-intel/
├── apps/
│   ├── backend/          # FastAPI backend
│   └── frontend/         # Next.js frontend
├── docs/                 # Дополнительная документация
├── infra/                # SQL и инфраструктура
└── scripts/              # Скрипты деплоя и запуска
```

## 🧪 Полезные команды

```bash
make run:backend           # Uvicorn backend с hot reload
make run:frontend          # Next.js dev сервер
python start_backend.py    # Полноценный backend с планировщиком
pnpm -C apps/frontend build
pnpm -C apps/frontend start
```

## 📊 API

### Каналы
- `GET /api/channels` — список каналов
- `POST /api/channels` — добавление нового канала
- `POST /api/channels/{id}/fetch` — запуск вручную задания сбора постов

### Посты
- `GET /api/channels/{id}/posts` — список постов канала
- `POST /api/posts/{id}/summarize` — создание саммари

Полное описание API см. в `docs/API.md`.

## 🤝 Вклад в проект
- Форкните репозиторий
- Создайте ветку (`git checkout -b feature/my-feature`)
- Внесите правки и закоммитьте (`git commit -m "Add my feature"`)
- Откройте Pull Request

## 📝 Лицензия

Проект распространяется под лицензией MIT. См. файл `LICENSE`.

## 📞 Поддержка

Вопросы и предложения — через Issues в GitHub.

---

Сделано с ❤️ для аналитики Telegram каналов
