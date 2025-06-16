from sqlalchemy import Column, Integer, String, DateTime, JSON
from datetime import datetime
from app.core.config import Base


class PollingJob(Base):
    __tablename__ = "polling_jobs"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True, nullable=False)
    symbols = Column(JSON, nullable=False)  # stores list of symbols
    interval = Column(Integer, nullable=False)
    provider = Column(String, nullable=False)
    max_runs = Column(Integer, nullable=False)
    status = Column(
        String, default="running"
    )  # could be 'running', 'completed', 'failed'
    created_at = Column(DateTime, default=datetime.utcnow)
