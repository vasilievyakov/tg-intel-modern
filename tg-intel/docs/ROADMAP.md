# План запуска MVP (Telegram Intelligence Platform)

## Фаза 0 — Инициализация окружений и репо

1. Создай пустой монорепо `tg-intel` (2 пакета: `apps/frontend`, `apps/backend`, плюс `/infra`):

* **Артефакты:** репозиторий GitHub, ветка `main`, базовый README.
* **Проверка:** `git status` чистый, CI запускается (GitHub Actions placeholder).

2. Заведи аккаунты и проекты:

* **Vercel** (для фронта), **Railway** (для бэка), **Supabase** (Postgres).
* **Артефакты:** project IDs, database URL, service role key (Supabase), Railway service URL.
* **Проверка:** доступ к консоли Supabase; в Railway — пустой сервис создан.

3. Создай единый `.env.example` в корне и симлинки для приложений:

```


# telegram (MTProto/Telethon)
TG_API_ID=
TG_API_HASH=
TG_SESSION_PATH=./.secrets/telethon.session
TG_PROXY_URL=  # опционально socks5/http(s)

# backend
BACKEND_PORT=8000
CRON_FETCH_MINUTES=5
AI_SUMMARY_ENDPOINT=        # Replicate/HF proxy
AI_SUMMARY_MODEL_ID=# общие
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
SUPABASE_DB_URL=postgresql://...

# frontend
NEXT_PUBLIC_API_BASE=       # публичный URL backend (Railway)
```

* **Артефакты:** `.env.example`, `.secrets/` в `.gitignore`.
* **Проверка:** `dotenv-linter` проходит; секреты не попадают в git.

---

## Фаза 1 — База данных (Supabase/Postgres)

4. Применить DDL (таблицы `channels`, `posts`, `summaries`, `fetch_jobs`, индексы, триггер `tsvector`):

* **Действие:** выполнить SQL-скрипт в Supabase SQL Editor.
* **Артефакты:** созданные таблицы и индексы (GIN + сортировка по `posted_at`).
* **Проверка:** `select count(*) from information_schema.tables where table_name in ('channels','posts','summaries','fetch_jobs');` ⇒ 4; `explain analyze` на FTS-запросе использует `idx_posts_tsv`.

5. Создать минимальные политики безопасности (RLS off для server-side, только backend-ключи используют service role):

* **Артефакт:** зафиксированное решение: **в MVP — только серверный доступ** (без прямых клиентских ключей).
* **Проверка:** запросы с anon-ключом запрещены (или не используются вовсе).

---

## Фаза 2 — Backend (FastAPI + Telethon + APScheduler)

6. Скелет FastAPI:

```
apps/backend/
  app.py
  api/
    channels.py
    posts.py
    summaries.py
  core/
    config.py
    db.py          # asyncpg / psycopg + SQLAlchemy (по желанию)
    logger.py
  services/
    telegram.py    # Telethon client, fetch logic
    fetcher.py     # batch/warm режимы
    ai.py          # вызовы summarization
  models/          # dataclasses/pydantic схемы
```

* **Артефакты:** FastAPI приложение с OpenAPI `/docs`.
* **Проверка:** локально `uvicorn app:app --reload` доступно, `/healthz` ⇒ `200 OK`.

7. Подключение к БД и FTS:

* **Действие:** реализовать функции чтения/записи `channels`, `posts`, FTS-поиск `text_tsv @@ to_tsquery(...)`.
* **Проверка:** unit-тест на вставку поста и FTS-поиск (ожидается ≥1 результат).

8. Telethon клиент и первичная загрузка:

* **Действие:** init Telethon по `TG_API_ID/ HASH`; сохранить `telethon.session` в `.secrets/`.
* **Функции:**

  * `resolve_channel(url) -> tg_id, title`
  * `fetch_history(tg_id, limit=200) -> [messages]`
  * нормализация → вставка в `posts` (c `unique(channel_id, tg_message_id)`).
* **Проверка:** добавить тестовый канал, получить ≥1 пост в БД.

9. APScheduler (batch режим):

* **Действие:** периодическая задача `*/CRON_FETCH_MINUTES`:

  * Берёт все `channels.status='active'`
  * Тянет новые посты > max(tg_message_id) по каналу
  * Логирует метрики (в `fetch_jobs.stats`)
* **Проверка:** через 5 мин новые посты появляются; `fetch_jobs` фиксирует `finished_at` и `status='success'`.

10. API-контракты:

* `POST /api/channels` { tg_url } → создает запись и ставит фон. job на первичную загрузку.
* `GET  /api/channels` → список + статус.
* `GET  /api/channels/{id}/posts?query=&page=&page_size=` → лента/поиск.
* `POST /api/posts/{post_id}/summarize` { model? } → синхронный вызов AI + кэш в `summaries`.
* **Проверка (curl):**

  * `curl -X POST .../api/channels -d '{"tg_url":"https://t.me/durov"}'`
  * `curl .../api/channels`
  * `curl .../api/channels/1/posts?query=update`
  * `curl -X POST .../api/posts/42/summarize`

11. Деплой Backend на Railway:

* **Действие:** Dockerfile или Buildpack; проставить ENV; монтировать `.secrets` как переменные/volume.
* **Артефакты:** публичный URL бэкенда, живой `/healthz`.
* **Проверка:** Swagger доступен извне; тайминги p95 API < 300 мс для FTS (на тестовых 5–10k постов).

---

## Фаза 3 — Frontend (Next.js + TypeScript + Tailwind + shadcn/ui)

12. Инициализация Next.js:

* `apps/frontend` со страницами:

  * `/` — список каналов, модалка «Добавить канал»
  * `/channels/[id]` — лента постов + строка поиска + пагинация
* **Компоненты shadcn/ui:** `Button`, `Input`, `Table`, `Dialog`, `Badge`, `Toast`, `Skeleton`.
* **Проверка:** локально `pnpm dev` открывает каркас; заглушки рендерятся.

13. Интеграция с API:

* **Действие:** обёртки `api/*.ts` для вызовов backend; `.env` с `NEXT_PUBLIC_API_BASE`.
* **UX-детали:** optimistic UI при добавлении канала; polling статуса до `active`.
* **Проверка:** добавление канала из фронта создаёт запись и запускает первичную загрузку; лента показывает посты.

14. Деплой Frontend на Vercel:

* **Действие:** подключить репо, задать env, включить Preview deployments.
* **Проверка:** прод-URL доступен; кросс-origin вызовы к backend успешны (CORS настроен).

---

## Фаза 4 — AI-саммари

15. Выбор провайдера (Replicate/HF Inference) и тонкой обёртки:

* **Действие:** `services/ai.py`: `summarize(text, model_id, max_tokens, lang='ru')`.
* **Политика:** вызывать только для постов `len(text) > 500` и только «по кнопке» (on-demand).
* **Кэш:** `summaries(post_id)` — уникальный key; повторные вызовы не бьют по бюджету.
* **Проверка:** 3 длинных поста → 3 успешных саммари, повторные запросы отдают кэш < 50 мс.

---

## Фаза 5 — Наблюдаемость и эксплуатация

16. Логирование и метрики:

* **Действие:** структурные логи (JSON), базовые метрики в БД (`fetch_jobs.stats`), простой `/metrics` endpoint (по возможности).
* **Пороговые алерты (пока вручную):**

  * `ingest_success_ratio < 0.9` за 15 мин
  * `flood_wait_rate > 0.03` за час
  * `sessions_alive == 0`
* **Проверка:** искусственно вызвать FLOOD_WAIT, убедиться, что лог и счётчик увеличились.

17. Rate-limit и сессии:

* **Действие:** задержки между запросами, журнал FLOOD_WAIT, бэкофф, опциональная прокси-ротация.
* **Проверка:** длительный прогон на 10–20 каналах без бана и сессия живёт > 24h.

---

## Фаза 6 — Тестовые данные и приемка

18. Seed-набор:

* **Действие:** добавить 5–10 публичных каналов (разные тематики), прогнать первичную загрузку (200 сообщений каждый).
* **Проверка:** суммарно ≥ 5k постов; FTS-поиск выдаёт результаты ≤ 300 мс (p95).

19. E2E-проверка пользовательских историй:

* Добавление канала, ожидание «active»
* Поиск по ключу и чтение постов
* Саммари длинного поста
* **Критерии готовности MVP:** все 3 сценария стабильны; UI без критических багов.

---

## Фаза 7 — Документация и хенд-офф

20. Обнови README и добавь:

* `docs/ARCHITECTURE.md` (диаграмма потоков warm/batch)
* `docs/DEPLOY.md` (Vercel/Railway/Supabase шаги)
* `docs/API.md` (с примерами curl)
* `.env.example` с комментариями
* **Проверка:** новый разработчик поднимает проект за ≤ 60 минут.

---

# Контрольный список для ИИ-исполнителя (в сжатом виде)

* [ ] создать монорепо и базовые папки
* [ ] подключить Vercel/Railway/Supabase, заполнить `.env.example`
* [ ] применить DDL в Supabase, проверить индексы и триггеры
* [ ] поднять FastAPI, подключить БД, реализовать FTS
* [ ] интегрировать Telethon: resolve, history(200), инкрементальные апдейты
* [ ] включить APScheduler (`CRON_FETCH_MINUTES`)
* [ ] реализовать API: `channels`, `posts`, `summaries`
* [ ] задеплоить backend на Railway, проверить `/docs`
* [ ] инициализировать Next.js + shadcn/ui; реализовать 2 экрана и запросы
* [ ] задеплоить фронт на Vercel, прописать CORS
* [ ] подключить AI-саммари и кэш в БД
* [ ] включить логи/метрики/пороговые проверки
* [ ] прогнать seed-набор из 5–10 каналов, e2e-сценарии, зафиксировать SLA/SLO

Упакуй это в `docs/ROADMAP.md` и добавь готовые скрипты (`make init`, `make migrate`, `make run:dev`, `make deploy:*`)


