from sqlalchemy.orm import Session
from ..models import Snapshot

def write_snapshot(db: Session, service: str, metric: str, payload: dict) -> None:
    snapshot = Snapshot(service=service, metric=metric, payload=payload)
    db.add(snapshot)
    db.commit()
