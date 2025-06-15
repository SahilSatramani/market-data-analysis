from fastapi import APIRouter, Query
from app.services.provider import fetch_price
from app.schemas.price import PriceResponse
from app.schemas.poll import PollingRequest, PollingResponse
from app.services.polling_api import start_polling_job_logic


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