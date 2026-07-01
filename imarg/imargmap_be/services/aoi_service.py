import json

from core.database import get_db2



def validate_aoi(geometry):

    #conn = get_db1()
    
    conn = get_db2()
    cur = conn.cursor()

    try:

        geojson = json.dumps(geometry)

        # Area + Total POI Count
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
                ST_Area(
                    geography(aoi.geom)
                ) / 1000000 AS area_sqkm,

                (
                    SELECT COUNT(*)
                    FROM public."DEDUCE_BINDU_V1.7.1" p
                    WHERE ST_Intersects(
                        p.geom,
                        aoi.geom
                    )
                ) AS poi_count

            FROM aoi
            """,
            (geojson,)
        )

        summary = cur.fetchone()

        # Preview Points (first 100)
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
                ST_Y(
                    ST_Centroid(p.geom)
                ) AS latitude,

                ST_X(
                    ST_Centroid(p.geom)
                ) AS longitude

            FROM public."DEDUCE_BINDU_V1.7.1" p
            WHERE ST_Intersects(
                p.geom,
                (SELECT geom FROM aoi)
            )
            """,
            (geojson,)
        )

        preview_rows = cur.fetchall()

        return {
            "area_sqkm": float(
                summary["area_sqkm"] or 0
            ),
            "poi_count": int(
                summary["poi_count"] or 0
            ),
            "preview_count": len(
                preview_rows
            ),
            "preview_points": [
                {
                    "latitude": row["latitude"],
                    "longitude": row["longitude"]
                }
                for row in preview_rows
            ]
        }

    finally:

        cur.close()
        conn.close()