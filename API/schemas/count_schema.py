from pydantic import BaseModel
from typing import Dict, Optional


class CountResponse(BaseModel):
    user_id: int
    total_requests: int
    breakdown: Dict[str, int]
    is_limit_exceeded: bool
    limit: int