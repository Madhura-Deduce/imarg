FREE_AREA_LIMIT = 100
PREMIUM_AREA_LIMIT = 500


def get_area_limit(subscription_type: str):

    if subscription_type.lower() == "free":
        return FREE_AREA_LIMIT

    if subscription_type.lower() == "premium":
        return PREMIUM_AREA_LIMIT

    return 0