from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from core.dependencies import get_current_user
from services.user_service import get_user_profile

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/profile")
def profile(user=Depends(get_current_user)):

    profile = get_user_profile(user["user_id"])

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Don't expose password
    profile.pop("password", None)

    # Convert datetime fields
    if profile.get("created_at"):
        profile["created_at"] = profile["created_at"].isoformat()

    if profile.get("subscription_expiry"):
        profile["subscription_expiry"] = (
            profile["subscription_expiry"].isoformat()
        )

    return {
        "success": True,
        "data": profile
    }