from fastapi import HTTPException

from core.database import admin_test

from core.config import (
    USER_REQUEST_LIMIT,
    API_KEY_REQUEST_LIMIT,
    IP_REQUEST_LIMIT,
    RATE_WINDOW_MINUTES,
    MAX_IPS_PER_USER,
    IP_ROTATION_WINDOW_MINUTES
)


def block_user(
        user_id,
        api_key,
        ip_address,
        request_count,
        reason
):

    conn = admin_test()
    cur = conn.cursor()

    try:

        # Store abuse history
        cur.execute(
            """
            INSERT INTO abuse_logs
            (
                user_id,
                api_key,
                ip_address,
                request_count,
                blocked_reason
            )
            VALUES
            (
                %s,%s,%s,%s,%s
            )
            """,
            (
                user_id,
                api_key,
                ip_address,
                request_count,
                reason
            )
        )
        #print("absue called")

        # Block user
        cur.execute(
            """
            UPDATE users
            SET
                is_active = FALSE,
                is_blocked = TRUE,
                api_key = NULL
            WHERE id=%s
            """,
            (user_id,)
        )

        conn.commit()

    finally:

        cur.close()
        conn.close()

#("check abuse")
def check_abuse(
        user_id,
        api_key,
        ip_address
):

    conn = admin_test()
    cur = conn.cursor()

    try:

        
        # USER LIMIT
        
        cur.execute(
            f"""
            SELECT COUNT(*)
            FROM api_usage_logs
            WHERE user_id=%s
            AND request_time >
            NOW() - interval '{RATE_WINDOW_MINUTES} minute'
            """,
            (user_id,)
        )

        user_count = cur.fetchone()["count"]

        if user_count > USER_REQUEST_LIMIT:

            block_user(
                user_id,
                api_key,
                ip_address,
                user_count,
                "USER_RATE_LIMIT_EXCEEDED"
            )

            raise HTTPException(
                status_code=403,
                detail="USER_RATE_LIMIT_EXCEEDED"
            )

        
        # API KEY LIMIT
        
        cur.execute(
            f"""
            SELECT COUNT(*)
            FROM api_usage_logs
            WHERE api_key=%s
            AND request_time >
            NOW() - interval '{RATE_WINDOW_MINUTES} minute'
            """,
            (api_key,)
        )

        api_count = cur.fetchone()["count"]

        if api_count > API_KEY_REQUEST_LIMIT:

            block_user(
                user_id,
                api_key,
                ip_address,
                api_count,
                "API_KEY_RATE_LIMIT_EXCEEDED"
            )

            raise HTTPException(
                status_code=403,
                detail="API_KEY_RATE_LIMIT_EXCEEDED"
            )

        
        # IP LIMIT
        
        cur.execute(
            f"""
            SELECT COUNT(*)
            FROM api_usage_logs
            WHERE ip_address=%s
            AND request_time >
            NOW() - interval '{RATE_WINDOW_MINUTES} minute'
            """,
            (ip_address,)
        )

        ip_count = cur.fetchone()["count"]

        if ip_count > IP_REQUEST_LIMIT:

            block_user(
                user_id,
                api_key,
                ip_address,
                ip_count,
                "IP_RATE_LIMIT_EXCEEDED"
            )

            raise HTTPException(
                status_code=403,
                detail="IP_RATE_LIMIT_EXCEEDED"
            )

        
        # API KEY SHARING
        
        cur.execute(
            f"""
            SELECT COUNT(DISTINCT ip_address)
            FROM api_usage_logs
            WHERE user_id=%s
            AND request_time >
            NOW() - interval '{IP_ROTATION_WINDOW_MINUTES} minute'
            """,
            (user_id,)
        )

        ip_used = cur.fetchone()["count"]

        if ip_used > MAX_IPS_PER_USER:

            block_user(
                user_id,
                api_key,
                ip_address,
                ip_used,
                "API_KEY_SHARING_DETECTED"
            )

            raise HTTPException(
                status_code=403,
                detail="API_KEY_SHARING_DETECTED"
            )

    finally:

        cur.close()
        conn.close()