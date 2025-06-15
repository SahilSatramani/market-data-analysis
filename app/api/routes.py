from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.provider import fetch_price
from app.schemas.price import PriceResponse
from app.schemas.poll import PollingRequest, PollingResponse
from app.services.polling_api import start_polling_job_logic
from app.models.symbol_average import SymbolAverage
from app.core.config import get_db


router = APIRouter()

@router.get("/prices/latest", response_model=PriceResponse)
async def get_latest_price(symbol: str = Query(...), provider: str = Query("alpha_vantage")):
    return await fetch_price(symbol, provider)

@router.post("/prices/poll", response_model=PollingResponse)
async def start_polling(request: PollingRequest):
    job_id = await start_polling_job_logic(request)
    return PollingResponse(
        job_id=job_id,
        status="accepted",
        config=request
    )

@router.get("/prices/average")
def get_symbol_average(symbol: str, db: Session = Depends(get_db)):
    record = db.query(SymbolAverage).filter_by(symbol=symbol).first()
    if not record:
        raise HTTPException(status_code=404, detail="Symbol not found")
    
    return {
        "symbol": record.symbol,
        "average_price": record.average_price,
        "updated_at": record.updated_at
    }