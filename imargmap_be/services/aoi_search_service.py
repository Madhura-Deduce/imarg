# services/aoi_search_service.py
#unused file
import json

from core.database import get_aoi_db


def get_features_in_aoi(geometry):

    conn = get_aoi_db()
    cur = conn.cursor()

    try:

        geojson = json.dumps(geometry)

        query = """
        SELECT
            osm_id,
            name,
            amenity,

            ST_X(ST_Transform(way,4326))
                AS longitude,

            ST_Y(ST_Transform(way,4326))
                AS latitude

        FROM planet_osm_point

        WHERE ST_Intersects(
            way,

            ST_Transform(
                ST_SetSRID(
                    ST_GeomFromGeoJSON(%s),
                    4326
                ),
                3857
            )
        )
        """

        cur.execute(
            query,
            (geojson,)
        )

        return cur.fetchall()

    finally:
        cur.close()
        conn.close()