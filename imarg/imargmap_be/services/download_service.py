import json

from core.database import get_db1

from core.database import get_db2


def can_download(user_id):

    conn = get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT 1
            FROM users
            WHERE id = %s
            AND subscription_type = 'PREMIUM'
            AND subscription_expiry IS NOT NULL
            AND subscription_expiry > NOW()
            """,
            (user_id,)
        )

        return cur.fetchone() is not None

    finally:
        cur.close()
        conn.close()

def get_selected_pois(geometry):

    conn = get_db2()
    cur = conn.cursor()

    try:

        geojson = json.dumps(geometry)

        cur.execute(
            """
            WITH aoi AS (
                SELECT
                    ST_SetSRID(
                        ST_GeomFromGeoJSON(%s),
                        4326
                    ) AS geom
            )

            SELECT
                *,
                ST_AsGeoJSON(p.geom) AS geometry_json

            FROM public."DEDUCE_BINDU_V1.7.1" p
            WHERE ST_Intersects(
                p.geom,
                (SELECT geom FROM aoi)
            )
            """,
            (geojson,)
        )

        return cur.fetchall()

    finally:
        cur.close()
        conn.close()
        
def get_download_count(geometry):

    conn = get_db2()
    cur = conn.cursor()

    try:

        geojson = json.dumps(geometry)

        cur.execute(
            """
            WITH aoi AS (
                SELECT
                    ST_SetSRID(
                        ST_GeomFromGeoJSON(%s),
                        4326
                    ) AS geom
            )

            SELECT COUNT(*) AS total

            FROM public."DEDUCE_BINDU_V1.7.1" p
            JOIN aoi
                ON ST_Intersects(
                    p.geom,
                    aoi.geom
                )
            """,
            (geojson,)
        )

        return cur.fetchone()["total"]

    finally:
        cur.close()
        conn.close()