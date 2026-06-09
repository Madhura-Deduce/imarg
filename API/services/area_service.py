from math import radians, sin, cos, sqrt, atan2

EARTH_RADIUS_KM = 6371


def haversine_distance(lat1, lon1, lat2, lon2):  #needs to be changed according to type of ploygon

    lat1 = radians(lat1)
    lon1 = radians(lon1)

    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        +
        cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return EARTH_RADIUS_KM * c
def calculate_bbox_area(
    min_lat,
    min_lon,
    max_lat,
    max_lon
):

    # height of rectangle
    height_km = haversine_distance(
        min_lat,
        min_lon,
        max_lat,
        min_lon
    )

    # width of rectangle
    width_km = haversine_distance(
        min_lat,
        min_lon,
        min_lat,
        max_lon
    )

    area_sqkm = height_km * width_km

    return round(area_sqkm, 2)