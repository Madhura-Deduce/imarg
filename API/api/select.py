from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from schemas.map_schema import BoundingBoxRequest

from services.area_service import calculate_area
from services.select_service import get_data_in_bbox

from dependencies import get_current_user

router = APIRouter()

@router.post("/select")
def select_data(
    request: BoundingBoxRequest,
    current_user=Depends(get_current_user)
):

    area = calculate_area(
        request.min_lat,
        request.min_lon,
        request.max_lat,
        request.max_lon
    )

    if current_user.plan == "free":
        limit = 100

    else:
        limit = 500

    if area > limit:

        raise HTTPException(
            status_code=403,
            detail=f"Selected area exceeds {limit} sq km"
        )

    results = get_data_in_bbox(
        request.min_lat,
        request.min_lon,
        request.max_lat,
        request.max_lon,
        MAP_DATA
    )

    return {
        "user_plan": current_user.plan,
        "area_sqkm": area,
        "selected_count": len(results),
        "results": results
    }