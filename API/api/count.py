from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import get_db
from models.request_log import RequestLog
from schemas.count_schema import CountResponse
from core.config import FREE_LIMIT, PREMIUM_LIMIT

# assuming you already have user dependency
from dependencies import get_current_user

router = APIRouter()
@router.get("/count", response_model=CountResponse)
def count_user_requests(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    user_id = current_user["id"]
    plan = current_user["plan"]   # free / premium

    # STEP 1: total request count
    total_requests = db.query(RequestLog).filter(
        RequestLog.user_id == user_id
    ).count()

    # STEP 2: breakdown by action type
    breakdown_query = db.query(
        RequestLog.action_type,
        func.count(RequestLog.id)
    ).filter(
        RequestLog.user_id == user_id
    ).group_by(
        RequestLog.action_type
    ).all()

    breakdown = {action: count for action, count in breakdown_query}

    # STEP 3: decide limit
    limit = FREE_LIMIT if plan == "free" else PREMIUM_LIMIT

    # STEP 4: check limit exceeded
    is_limit_exceeded = total_requests > limit

    # STEP 5: response
    return CountResponse(
        user_id=user_id,
        total_requests=total_requests,
        breakdown=breakdown,
        is_limit_exceeded=is_limit_exceeded,
        limit=limit
    )