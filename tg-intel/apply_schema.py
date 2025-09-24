import os
from dotenv import load_dotenv
import psycopg

load_dotenv()
dsn = os.getenv('SUPABASE_DB_URL') or os.getenv('SUPABASE_URL')
with psycopg.connect(dsn, autocommit=True) as conn:
    with conn.cursor() as cur:
        cur.execute(open('infra/sql/schema.sql','r',encoding='utf-8').read())
print('SCHEMA_APPLIED')
