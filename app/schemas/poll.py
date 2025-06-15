from pydantic import BaseModel
from typing import List,Optional

class PollingRequest(BaseModel):
    symbols: List[str]
    interval: int  # in seconds
    provider: str = "alpha_vantage"
    max_runs: Optional[int] = 10

class PollingResponse(BaseModel):
    job_id: str
    status: str
    config: PollingRequest