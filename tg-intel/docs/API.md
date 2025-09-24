API reference (MVP)

Base URL: http://localhost:8000

Health

GET /healthz
200 { "status": "ok" }

Channels

POST /api/channels
Body: { "tg_url": "https://t.me/durov" }
201 { id, tg_url, title, status, created_at }

GET /api/channels
200 [ { id, tg_url, title, status, created_at }, ... ]

Posts

GET /api/channels/{id}/posts?query=&page=1&page_size=20
200 { items: Post[], page, page_size, total }

Summaries

POST /api/posts/{post_id}/summarize
200 { post_id, summary, cached }

Curl examples

Create channel
curl -X POST "$BASE/api/channels" -H "Content-Type: application/json" -d '{"tg_url":"https://t.me/durov"}'

List channels
curl "$BASE/api/channels"

Search posts
curl "$BASE/api/channels/1/posts?query=update"

Summarize
curl -X POST "$BASE/api/posts/42/summarize"


