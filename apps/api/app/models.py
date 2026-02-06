from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base

class ServiceHeartbeat(Base):
    __tablename__ = "service_heartbeat"

    service_name: Mapped[str] = mapped_column(String(50), primary_key=True)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ok")
    message: Mapped[str | None] = mapped_column(Text)


class SyncRun(Base):
    __tablename__ = "sync_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    source: Mapped[str] = mapped_column(String(30), nullable=False)  # steam|trakt
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    success: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    error: Mapped[str | None] = mapped_column(Text)

    items_fetched: Mapped[int] = mapped_column(Integer, default=0)
    items_written: Mapped[int] = mapped_column(Integer, default=0)
