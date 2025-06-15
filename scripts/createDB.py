from app.core.config import Base, engine
from app.models.raw_market_data import RawMarketData  # make sure this import exists!

# Create all tables
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")