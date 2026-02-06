import os
from fastapi import FastAPI
import psycopg

app = FastAPI(title="Dashboard API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/health/db")
def health_db():
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        return {"status": "error", "db": "missing DATABASE_URL"}

    try:
        # Connect and run a tiny query
        with psycopg.connect(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                cur.fetchone()
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "db": "connection_failed", "detail": str(e)}
