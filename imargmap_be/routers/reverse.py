#from fastapi import APIRouter, Query
#from core.database import get_db
from fastapi import APIRouter, Query, Request, Depends

from core.database import get_db
#from core.database import admin_test
from core.dependencies import get_current_user
#from services.request_counter_service import check_request_limit
from services.request_limit_service import check_request_limit
from services.audit_service import log_api_usage
from services.abuse_service import (
    check_abuse,
    is_ip_blocked
)

router = APIRouter(
    tags=["Reverse Geocoding"]
)


@router.get("/reverse")
def reverse_geocode(
    request: Request,
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    limit: int = Query(1, description="Number of nearest features"),
    user=Depends(get_current_user)
):
    print("inside reverse")
    conn = get_db()
    #conn = admin_test()
    cursor = conn.cursor()
    try:
        query = """
        SELECT 
            name, 
            amenity, 
            "addr:housename" AS housename, 
            "addr:housenumber" AS housenumber,
            tags -> 'landmark' AS landmark,
            tags -> 'addr:street' AS street,
            tags -> 'secon_sree' AS secondary_street,
            tags -> 'addr:hamlet' AS locality,
            tags -> 'addr:suburb' AS sublocality,
            tags -> 'state' AS state,
            tags -> 'addr:city' AS city,
            tags -> 'addr:postcode' AS postcode,
            tags -> 'website' AS website,
            tags -> 'mobile' AS mobile,
            tags -> 'days_of_wo' AS days,
            ST_Y(ST_Transform(way, 4326)) AS latitude, 
            ST_X(ST_Transform(way, 4326)) AS longitude,
            ST_Distance(
                ST_Transform(way, 3857),
                ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326), 3857)
            ) AS distance_meters,
            TRIM(BOTH ', ' FROM
                CONCAT_WS(', ',
                    CASE WHEN tags -> 'landmark' NOT IN ('', 'None') THEN tags -> 'landmark' END,
                    CASE WHEN tags -> 'addr:street' NOT IN ('', 'None') THEN tags -> 'addr:street' END,
                    CASE WHEN tags -> 'secon_sree' NOT IN ('', 'None') THEN tags -> 'secon_sree' END,
                    CASE WHEN tags -> 'addr:hamlet' NOT IN ('', 'None') THEN tags -> 'addr:hamlet' END,
                    CASE WHEN tags -> 'addr:suburb' NOT IN ('', 'None') THEN tags -> 'addr:suburb' END,
                    CASE WHEN tags -> 'addr:city' NOT IN ('', 'None') THEN tags -> 'addr:city' END,
                    CASE WHEN tags -> 'state' NOT IN ('', 'None') THEN tags -> 'state' END,
                    CASE WHEN tags -> 'addr:postcode' NOT IN ('', 'None') THEN tags -> 'addr:postcode' END
                )
            ) AS description
        FROM planet_osm_point
        WHERE way IS NOT NULL
        ORDER BY way <-> ST_Transform(ST_SetSRID(ST_MakePoint(%s, %s), 4326), 3857)
        LIMIT %s;
        """
        cursor.execute(query, (lon, lat, lon, lat, limit))
        results = cursor.fetchall()
        ip_address = request.client.host
        '''check_abuse(
            user_id=user["user_id"],
            ip_address=ip_address,
            api_key=user["api_key"]
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
            
            endpoint="/reverse"
        )

        check_request_limit(
            user["user_id"],
            user["api_key"],
            ip_address
        )

        

        return results or {"message": "No POI found near this location."}
    finally:
        cursor.close()
        conn.close()
