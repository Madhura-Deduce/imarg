from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database import get_db

from schemas.authorization_schema import AuthorizationRequest

from services.area_service import calculate_bbox_area
from services.authorization_service import get_area_limit

from dependencies import get_current_user

router = APIRouter(
    prefix="/authorization",
    tags=["Authorization"]
)

@router.post("/download-access")
def verify_download_access(
    request: AuthorizationRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    area = calculate_bbox_area(
        request.min_lat,
        request.min_lon,
        request.max_lat,
        request.max_lon
    )

    subscription_type = current_user.subscription_type

    allowed_limit = get_area_limit(
        subscription_type
    )

    if area > allowed_limit:

        return {
            "authorized": False,
            "can_download": False,
            "selected_area_sqkm": area,
            "allowed_limit_sqkm": allowed_limit,
            "message": (
                f"Selected area exceeds "
                f"{allowed_limit} sq km limit"
            )
        }

    return {
        "authorized": True,
        "can_download": True,
        "selected_area_sqkm": area,
        "allowed_limit_sqkm": allowed_limit,
        "message": "Download permitted"
    }