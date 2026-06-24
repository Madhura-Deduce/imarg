from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request #newly added

from core.dependencies import get_current_user
from services.abuse_service import check_abuse
from schemas.download import DownloadRequest

from core.rate_limit import (
    check_download_rate_limit
)

from services.audit_service import (
    log_download,
    log_api_usage
)

from services.download_service import (
    can_download
)

router = APIRouter(
    prefix="/download",
    tags=["Download"]
)


'''@router.post("")
def download_data(
    data: DownloadRequest,
    user=Depends(get_current_user)
):'''
@router.post("")
def download_data(
    request: Request,
    data: DownloadRequest,
    user=Depends(get_current_user)
):

    if user["subscription"] != "PREMIUM":

        raise HTTPException(
            status_code=403,
            detail="Premium subscription required"
        )

    allowed = can_download(
        user["user_id"]
    )

    if not allowed:

        raise HTTPException(
            status_code=403,
            detail="Payment required"
        )

    check_download_rate_limit(
        user["user_id"],
        user["subscription"]
    )

    if data.format not in [
        "geojson",
        "csv",
        "gpkg"
    ]:

        raise HTTPException(
            status_code=400,
            detail="Invalid format"
        )

    '''log_download(
        user["user_id"],
        data.format
    )'''
    ip_address = request.client.host

    log_download(
        user["user_id"],
        user["email"],
        user["api_key"],
        data.format,
        ip_address
)

    '''log_api_usage(
        user["user_id"],
        "/download"
    )'''
    log_api_usage(
    user["user_id"],
    user["api_key"],
    ip_address,
    "/download"
    )
    check_abuse(
    user["user_id"],
    user["api_key"],
    ip_address
    )

    return {
        "success": True,
        "message": f"{data.format} download allowed"
    }