from fastapi import FastAPI
from sqlalchemy import text

from app.db import engine

app = FastAPI(title="Dashboard API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def health_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "db": "connection_failed", "detail": str(e)}
