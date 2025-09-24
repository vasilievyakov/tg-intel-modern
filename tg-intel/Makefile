SHELL := /usr/bin/env bash

.PHONY: init run:backend run:frontend run:dev migrate deploy:backend deploy:frontend

init:
	python -m venv .venv || true
	. .venv/bin/activate && pip install -U pip wheel || true
	. .venv/bin/activate && pip install -r apps/backend/requirements.txt || true
	corepack enable || true
	pnpm -C apps/frontend install || true

run:backend:
	. .venv/bin/activate && uvicorn apps.backend.app:app --reload --port $${BACKEND_PORT:-8000}

run:frontend:
	pnpm -C apps/frontend dev

run:dev:
	@echo "Run backend and frontend in two terminals"

migrate:
	@echo "Open infra/sql/schema.sql in Supabase SQL Editor and apply."

deploy:backend:
	@echo "Deploy to Railway: set envs from .env.example and use apps/backend."
	@echo "1. Go to https://railway.app"
	@echo "2. Connect GitHub repository"
	@echo "3. Create new service from repository"
	@echo "4. Set environment variables from .env.example"
	@echo "5. Railway will auto-detect Dockerfile and deploy"

deploy:frontend:
	@echo "Deploy to Vercel: set NEXT_PUBLIC_API_BASE and connect repo."
	@echo "1. Go to https://vercel.com"
	@echo "2. Connect GitHub repository"
	@echo "3. Set root directory to 'apps/frontend'"
	@echo "4. Set NEXT_PUBLIC_API_BASE to your Railway backend URL"
	@echo "5. Vercel will auto-detect Next.js and deploy"

deploy:all:
	@echo "Deploy both backend and frontend"
	@echo "See docs/DEPLOY.md for detailed instructions"
	@echo "Run: make deploy:backend && make deploy:frontend"


