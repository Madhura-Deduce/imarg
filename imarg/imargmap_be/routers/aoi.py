from fastapi import APIRouter, Depends, Request

from schemas.aoi import ValidateAOIRequest

from services.aoi_service import validate_aoi

from core.dependencies import get_current_user

from services.audit_service import log_api_usage
from services.abuse_service import check_abuse
#from core.database import get_db


#from core.rate_limit import check_api_rate_limit
#newly added
from core.rate_limit import (
    check_api_rate_limit,
    check_area_limit
)

router = APIRouter(
    prefix="/aoi",
    tags=["AOI"]
)


'''@router.post("/validate")
def validate_polygon(
    data: ValidateAOIRequest,
    user=Depends(get_current_user)
):

    check_api_rate_limit(
        user["user_id"],
        user["subscription"]
    )

    result = validate_aoi(
        data.geometry
    )
    check_area_limit(result["area_sqkm"],user["subscription"])  #newly added

    log_api_usage(
        user["user_id"],
        "/aoi/validate"
    )

    if user["subscription"] == "FREE":

        return {
            "success": True,
            "area_sqkm": result["area_sqkm"],
            "point_count": result["point_count"],
            "subscription_type": "FREE",
            "download_allowed": False,
            "allowed_formats": [],
            "message": "Upgrade to Premium to download data"
        }

    return {
        "success": True,
        "area_sqkm": result["area_sqkm"],
        "point_count": result["point_count"],
        "subscription_type": "PREMIUM",
        "download_allowed": True,
        "allowed_formats": [
            "geojson",
            "csv",
            "gpkg"
        ]
    }'''
@router.post("/validate")
def validate_polygon(
    request: Request,
    data: ValidateAOIRequest,
    user=Depends(get_current_user)
):

    check_api_rate_limit(
        user["user_id"],
        user["subscription"]
    )

    result = validate_aoi(
        data.geometry
    )

    check_area_limit(
        result["area_sqkm"],
        user["subscription"]
    )

    ip_address = request.client.host

    log_api_usage(
        user["user_id"],
        user["api_key"],
        ip_address,
        "/aoi/validate"
    )

    check_abuse(
        user["user_id"],
        user["api_key"],
        ip_address
    )

    if user["subscription"] == "FREE":

        return {
            "success": True,
            "area_sqkm": result["area_sqkm"],
            "point_count": result["point_count"],
            "subscription_type": "FREE",
            "download_allowed": False,
            "allowed_formats": [],
            "message": "Upgrade to Premium to download data"
        }

    return {
        "success": True,
        "area_sqkm": result["area_sqkm"],
        "point_count": result["point_count"],
        "subscription_type": "PREMIUM",
        "download_allowed": True,
        "allowed_formats": [
            "geojson",
            "csv",
            "gpkg"
        ]
    }