# routers/aoi_search.py

from fastapi import APIRouter

from schemas.aoi import ValidateAOIRequest

from services.aoi_search_service import (
    get_features_in_aoi
)

router = APIRouter(
    prefix="/aoi",
    tags=["AOI"]
)


@router.post("/features")
def get_features(data: ValidateAOIRequest):

    results = get_features_in_aoi(
        data.geometry
    )

    return {
        "count": len(results),
        "features": results
    }