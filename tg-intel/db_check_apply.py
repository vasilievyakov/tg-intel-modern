import os, sys
from dotenv import load_dotenv
import psycopg

load_dotenv()
dsn = os.getenv('SUPABASE_DB_URL')
if not dsn:
    print('ERR:NO_DSN')
    sys.exit(1)

with psycopg.connect(dsn, autocommit=True) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            select table_name from information_schema.tables
            where table_schema='public' and table_name in ('channels','posts','summaries','fetch_jobs')
        """)
        existing = {r[0] for r in cur.fetchall()}
        print('EXISTING:', sorted(existing))
        if existing >= {'channels','posts','summaries','fetch_jobs'}:
            print('SCHEMA_OK')
            sys.exit(0)

# Apply schema if missing
schema_path = 'infra/sql/schema.sql'
sql = open(schema_path, 'r', encoding='utf-8').read()
# naive split by ; keeping statements simple
stmts = []
acc = []
for line in sql.splitlines():
    s = line.strip()
    if not s or s.startswith('--'):
        continue
    acc.append(line)
    if s.endswith(';'):
        stmts.append('\n'.join(acc))
        acc = []
if acc:
    stmts.append('\n'.join(acc))

applied = 0
with psycopg.connect(dsn, autocommit=True) as conn:
    with conn.cursor() as cur:
        for st in stmts:
            try:
                cur.execute(st)
                applied += 1
            except Exception as e:
                print('APPLY_ERR:', type(e).__name__, str(e)[:200])
print('APPLIED_COUNT:', applied)
print('DONE')
