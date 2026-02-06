docker compose -f infra/docker-compose.yml exec api python - << "EOF"
from app.db import engine
from sqlalchemy import text

with engine.connect() as c:
    print(c.execute(text("select 1")).scalar())
EOF
