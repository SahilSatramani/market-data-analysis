from app.core.config import Base, engine
from app.models.raw_market_data import RawMarketData 
from app.models.polling_job import PollingJob
from app.models.symbol_average import SymbolAverage  

# Create all tables
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")