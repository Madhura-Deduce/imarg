import io
import csv
import json
import tempfile
import os
import tempfile
import geopandas as gpd

from shapely.geometry import shape

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request #newly added
from services.request_limit_service import check_request_limit

from fastapi.responses import (
    StreamingResponse,
    FileResponse
)

from core.dependencies import get_current_user
from services.abuse_service import (
    #check_abuse,
    is_ip_blocked
)
from core.rate_limit import check_download_rate_limit

from schemas.download import DownloadRequest

from services.audit_service import (
    log_download,
    log_api_usage
)

from services.download_service import (
    can_download,
    get_selected_pois
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
    ip_address = request.client.host

    
    allowed = can_download(
        user["user_id"]
    )

    if not allowed:

        raise HTTPException(
            status_code=403,
            detail=(
                "Premium subscription required "
                "or subscription expired"
            )
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

    pois = get_selected_pois(
        data.geometry
    )

    if not pois:

        raise HTTPException(
            status_code=404,
            detail="No POIs found in selected area"
        )

    '''log_download(
        user["user_id"],
        data.format
    )'''
    ip_address = request.client.host

    log_download(
        user["user_id"],
        user["email"],
        #user["api_key"],
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
    '''check_abuse(
    user["user_id"],
    user["api_key"],
    ip_address
    )'''

    #
    # GEOJSON
    #
    if data.format == "geojson":

        features = []

        for poi in pois:

            features.append(
                {
                    "type": "Feature",
                    "geometry": json.loads(
                        poi["geometry_json"]
                    ),
                    "properties": {
                        k: v
                        for k, v in poi.items()
                        if k not in [
                            "geom",
                            "geometry_json"
                        ]
                    }
                }
            )

        geojson_data = {
            "type": "FeatureCollection",
            "features": features
        }

        return StreamingResponse(
            io.StringIO(
                json.dumps(
                    geojson_data
                )
            ),
            media_type="application/geo+json",
            headers={
                "Content-Disposition":
                "attachment; filename=pois.geojson"
            }
        )

    #
    # CSV
    #
    if data.format == "csv":

        output = io.StringIO()

        columns = [
            key
            for key in pois[0].keys()
            if key not in [
                "geom",
                "geometry_json"
            ]
        ]

        writer = csv.DictWriter(
            output,
            fieldnames=columns
        )

        writer.writeheader()

        for row in pois:

            writer.writerow(
                {
                    k: v
                    for k, v in row.items()
                    if k in columns
                }
            )

        output.seek(0)

        return StreamingResponse(
            output,
            media_type="text/csv",
            headers={
                "Content-Disposition":
                "attachment; filename=pois.csv"
            }
        )

    
    # GPKG
    
    if data.format == "gpkg":

        records = []

        for poi in pois:

            record = {
                k: v
                for k, v in poi.items()
                if k not in [
                    "geom",
                    "geometry_json"
                ]
            }

            record["geometry"] = shape(
                json.loads(
                    poi["geometry_json"]
                )
            )

            records.append(record)

        gdf = gpd.GeoDataFrame(
            records,
            geometry="geometry",
            crs="EPSG:4326"
        )

        fd, gpkg_path = tempfile.mkstemp(
            suffix=".gpkg"
        )

        os.close(fd)

        os.remove(gpkg_path)

        gdf.to_file(
            gpkg_path,
            driver="GPKG",
            layer="pois"
        )

        return FileResponse(
            path=gpkg_path,
            filename="pois.gpkg",
            media_type="application/geopackage+sqlite3"
        )