-- Extensions
create extension if not exists pg_trgm;
create extension if not exists unaccent;

-- Channels
create table if not exists channels (
  id bigserial primary key,
  tg_id bigint unique,
  tg_url text unique not null,
  title text,
  status text not null default 'pending',
  created_at timestamptz not null default now()
);

-- Posts
create table if not exists posts (
  id bigserial primary key,
  channel_id bigint not null references channels(id) on delete cascade,
  tg_message_id bigint not null,
  posted_at timestamptz,
  text text,
  raw jsonb,
  text_tsv tsvector,
  unique(channel_id, tg_message_id)
);

create index if not exists idx_posts_channel_posted_at on posts(channel_id, posted_at desc);
create index if not exists idx_posts_tsv on posts using gin(text_tsv);

create or replace function posts_tsvector_trigger() returns trigger language plpgsql as $$
begin
  new.text_tsv :=
    setweight(to_tsvector('simple', coalesce(new.text, '')), 'B');
  return new;
end;
$$;

drop trigger if exists posts_tsvector_update on posts;
create trigger posts_tsvector_update before insert or update
  on posts for each row execute function posts_tsvector_trigger();

-- Summaries
create table if not exists summaries (
  id bigserial primary key,
  post_id bigint not null unique references posts(id) on delete cascade,
  model_id text,
  summary text,
  tokens int,
  created_at timestamptz not null default now()
);

-- Fetch jobs
create table if not exists fetch_jobs (
  id bigserial primary key,
  channel_id bigint references channels(id) on delete cascade,
  started_at timestamptz,
  finished_at timestamptz,
  status text,
  stats jsonb,
  error text
);
create index if not exists idx_fetch_jobs_channel on fetch_jobs(channel_id);
create index if not exists idx_fetch_jobs_started_at on fetch_jobs(started_at desc);


