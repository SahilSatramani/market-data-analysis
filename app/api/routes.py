from fastapi import APIRouter, Query
from app.services.provider import fetch_price
from app.schemas.price import PriceResponse

router = APIRouter()

@router.get("/prices/latest", response_model=PriceResponse)
async def get_latest_price(symbol: str = Query(...), provider: str = Query("alpha_vantage")):
    return await fetch_price(symbol, provider)