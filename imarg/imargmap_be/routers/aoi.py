from fastapi import APIRouter, Depends, Request

from fastapi import HTTPException
from fastapi import Depends

from core.dependencies import get_current_user
from services.request_limit_service import check_request_limit
from schemas.aoi import ValidateAOIRequest
from services.aoi_service import validate_aoi
from services.audit_service import log_api_usage
from services.abuse_service import (
    check_abuse,
    is_ip_blocked
)
#from core.database import get_db


#from core.rate_limit import check_api_rate_limit
#newly added

MAX_AREA_SQKM = 10

router = APIRouter(
    prefix="/aoi",
    tags=["AOI"]
)



@router.post("/validate")
def validate_polygon(
    request: Request,
    data: ValidateAOIRequest,
    user=Depends(get_current_user)
):

    try:

        result = validate_aoi(
            data.geometry
        )

        area_sqkm = round(
            result["area_sqkm"],
            2
        )

        ip_address = request.client.host
        
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

        '''log_api_usage(
            user["user_id"],
            "/aoi/validate"
        )'''

        return {
                "success": True,
                "area_sqkm": area_sqkm,
                "poi_count": result["poi_count"],
                "preview_count": result["preview_count"],
                "preview_points": result["preview_points"],
                "max_allowed_area_sqkm": MAX_AREA_SQKM,
                "message": "AOI validated successfully."
            }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )