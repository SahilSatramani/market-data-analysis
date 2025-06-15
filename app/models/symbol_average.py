from sqlalchemy import Column, String, Float, DateTime
from datetime import datetime
from app.core.config import Base

class SymbolAverage(Base):
    __tablename__ = "symbol_averages"

    symbol = Column(String, primary_key=True, index=True)
    average_price = Column(Float, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)