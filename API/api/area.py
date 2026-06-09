from fastapi import APIRouter

from schemas.map_schema import BoundingBoxRequest
from services.area_service import calculate_bbox_area

router = APIRouter(
    prefix="/area",
    tags=["Area"]
)

@router.post("/calculate")
def calculate_area(
    request: BoundingBoxRequest
):

    area = calculate_bbox_area(
        request.min_lat,
        request.min_lon,
        request.max_lat,
        request.max_lon
    )

    return {
        "area_sqkm": area
    }