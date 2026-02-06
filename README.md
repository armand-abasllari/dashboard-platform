# My Dashboard — Platform (API + DB + Collector)

Backend platform for `dashboard.abasllari.com`:
- FastAPI API (serves normalized data to the UI)
- Postgres database (stores snapshots/events + sync metadata)
- Collector (scheduled jobs that fetch Steam/Trakt/etc and writes to DB)

## Stack
- `dashboard-api` (FastAPI): http://localhost:8000
- `dashboard-db` (Postgres)
- `dashboard-collector` (placeholder for now)

## Quickstart (local, Windows + Docker Desktop)
1) Create env file:
- Copy `infra/.env.example` → `infra/.env`

2) Start stack:
```bash
cd infra
docker compose up -d --build

API:

http://localhost:8000/health

http://localhost:8000/health/db


Dev note (Windows + Docker Desktop)

If containers break randomly:

wsl --shutdown