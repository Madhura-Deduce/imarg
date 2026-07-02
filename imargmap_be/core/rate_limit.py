from fastapi import HTTPException

from core.database import get_db1



from fastapi import HTTPException



'''def check_api_rate_limit(
    user_id,
    subscription
):

    conn = get_db1()
    cur = conn.cursor()

    try:

        if subscription == "FREE":
            limit = 30
        else:
            limit = 100

        cur.execute(
            """
            SELECT COUNT(*)
            FROM api_usage_logs
            WHERE user_id=%s
            AND request_time >
                NOW() - interval '1 minute'
            """,
            (user_id,)
        )

        count = cur.fetchone()["count"]

        if count >= limit:

            cur.execute(
                """
                UPDATE users
                SET
                    is_active = FALSE,
                    api_key = NULL
                WHERE id=%s
                """,
                (user_id,)
            )

            conn.commit()

            raise HTTPException(
                status_code=403,
                detail="API limit exceeded. User blocked."
            )

    finally:
        cur.close()
        conn.close()'''


def check_download_rate_limit(
    user_id,
    subscription
):

    conn = get_db1()
    cur = conn.cursor()
    

    try:

        if subscription == "FREE":
            limit = 0
        else:
            limit = 100

        cur.execute(
            """
            SELECT COUNT(*)
            FROM download_logs
            WHERE user_id=%s
            AND downloaded_at >= CURRENT_DATE
            """,
            (user_id,)
        )

        count = cur.fetchone()["count"]

        if count >= limit:
            raise HTTPException(
                status_code=429,
                detail="Daily download limit exceeded"
            )

    finally:
        cur.close()
        conn.close()


def check_area_limit(
    area_sqkm,
    subscription
):

    if subscription == "FREE":

        limit = 100

    elif subscription == "PREMIUM":

        limit = 500

    else:

        raise HTTPException(
            status_code=400,
            detail="Invalid subscription type"
        )

    if area_sqkm > limit:

        raise HTTPException(
            status_code=400,
            detail=f"Maximum allowed area is {limit} sqkm"
        )