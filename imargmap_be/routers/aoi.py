from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from services.request_limit_service import check_request_limit

from core.dependencies import get_current_user
#from services.request_counter_service import check_request_limit
from schemas.aoi import ValidateAOIRequest
from services.aoi_service import validate_aoi
from services.audit_service import log_api_usage
from services.abuse_service import (
    check_abuse,
    is_ip_blocked
)
from fastapi import Request
#from core.database import get_db


#
MAX_AREA_SQKM = 10
#newly added
from core.rate_limit import check_area_limit


router = APIRouter(
    prefix="/aoi",
    tags=["AOI"]
)


'''@router.post("/validate")
def validate_polygon(
    data: ValidateAOIRequest,
    user=Depends(get_current_user)
):

    try:

        result = validate_aoi(
            data.geometry
        )
    check_area_limit(result["area_sqkm"],user["subscription"])  #newly added

        area_sqkm = round(
            result["area_sqkm"],
            2
        )

        if area_sqkm > MAX_AREA_SQKM:

            return {
                "success": False,
                "area_sqkm": area_sqkm,
                "poi_count": 0,
                "max_allowed_area_sqkm": MAX_AREA_SQKM,
                "message": (
                    f"Selected area exceeds the maximum "
                    f"allowed limit of {MAX_AREA_SQKM} sq km."
                )
            }

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

    try:

        '''check_api_rate_limit(
            user["user_id"],
            user["subscription"]
        )'''
        result = validate_aoi(
            data.geometry
        )

        check_area_limit(
            result["area_sqkm"],
            user["subscription"]
        )

        area_sqkm = round(
            result["area_sqkm"],
            2
        )

        ip_address = request.client.host
        '''check_abuse(
            user["user_id"],
            user["api_key"],
            ip_address
        )'''
        if is_ip_blocked(ip_address):
            raise HTTPException(
                  status_code=403,
                  detail="IP_BLOCKED"
            )
        
        log_api_usage(
            user_id=user["user_id"],
            api_key=user["api_key"],
            ip_address=ip_address,
            
            endpoint="/aoi/validate"
            
            
        )
        check_request_limit(
            user["user_id"],
            user["api_key"],
            ip_address
        )

        

        return {
            "success": True,
            "area_sqkm": area_sqkm,
            "poi_count": result["poi_count"],
            "preview_count": result["preview_count"],
            "preview_points": result["preview_points"],
            "max_allowed_area_sqkm": MAX_AREA_SQKM,
            "message": "AOI validated successfully."
        }
    except HTTPException:
        raise
    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )