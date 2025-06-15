import requests
from datetime import datetime
import os

#API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

#print("🔐 API Key from ENV:", os.getenv("ALPHA_VANTAGE_API_KEY"))

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

        return {
            "symbol": quote.get("01. symbol", symbol),
            "price": float(quote["05. price"]),
            "timestamp": datetime.utcnow(),
            "provider": "alpha_vantage"
        }

    else:
        raise ValueError("Unsupported provider")