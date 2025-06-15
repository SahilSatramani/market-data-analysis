import requests
from datetime import datetime
import os
from app.models.raw_market_data import RawMarketData
from app.core.config import SessionLocal
from sqlalchemy.exc import SQLAlchemyError
from app.kafka.producer import publish_price_event

async def fetch_price(symbol: str, provider: str):
    if provider == "alpha_vantage":
        API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": API_KEY
        }

        response = requests.get(url, params=params)

        try:
            data = response.json()
            print("Raw Alpha Vantage response:", data)
        except Exception as e:
            print("Error parsing JSON:", e)
            print("Raw response:", response.text)
            raise

        if "Global Quote" not in data or not data["Global Quote"]:
            raise ValueError(f"Alpha Vantage response missing 'Global Quote': {data}")

        quote = data["Global Quote"]
        price = float(quote["05. price"])

        # Save to database
        db = SessionLocal()
        try:
            record = RawMarketData(
                symbol=quote.get("01. symbol", symbol),
                price=price,
                timestamp=datetime.utcnow(),
                provider=provider,
                raw_response=data
            )
            db.add(record)
            db.commit()
            db.refresh(record)
            print("Data saved to DB with ID:", record.id)
        except SQLAlchemyError as e:
            db.rollback()
            print("DB Error:", str(e))
            raise
        finally:
            db.close()
        
        event = {
            "symbol": quote.get("01. symbol", symbol),
            "price": price,
            "timestamp": datetime.utcnow().isoformat(),
            "provider": provider,
            "raw": quote
        }
        publish_price_event(event)    

        # Return response for API
        return {
            "symbol": quote.get("01. symbol", symbol),
            "price": price,
            "timestamp": datetime.utcnow(),
            "provider": "alpha_vantage"
        }

    else:
        raise ValueError("Unsupported provider")