from app.core.config import Base, engine

from app.models.raw_market_data import RawMarketData  # noqa: F401
from app.models.symbol_average import SymbolAverage  # noqa: F401
from app.models.polling_job import PollingJob  # noqa: F401

# Create all tables
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
