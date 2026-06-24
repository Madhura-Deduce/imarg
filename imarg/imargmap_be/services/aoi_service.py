import json

from core.database import get_db1
#from core.database import get_aoi_db
#from core.database import admin_test

def validate_aoi(geometry):

    #conn = get_db1()
    '''conn = get_aoi_db()
    cur = conn.cursor()'''
    conn = get_db1()
    cur = conn.cursor()

    try:

        geojson = json.dumps(geometry)

        cur.execute(
            """
            SELECT
                ST_Area(
                    geography(
                        ST_SetSRID(
                            ST_GeomFromGeoJSON(%s),
                            4326
                        )
                    )
                ) / 1000000 AS area_sqkm,

                ST_NPoints(
                    ST_SetSRID(
                        ST_GeomFromGeoJSON(%s),
                        4326
                    )
                ) AS point_count
            """,
            (
                geojson,
                geojson
            )
        )

        return cur.fetchone()

    finally:
        cur.close()
        conn.close()