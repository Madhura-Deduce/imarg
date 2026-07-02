from fastapi import HTTPException
from datetime import datetime
from core.database import get_db1
from services.abuse_service import (
    block_user,
    is_ip_blocked
)

MAX_REQUESTS = 30


def check_request_limit(
        user_id,
        api_key,
        ip_address
):

    #
    # already blocked?
    #
    if is_ip_blocked(ip_address):

        raise HTTPException(
            status_code=403,
            detail="IP_BLOCKED"
        )

    conn = get_db1()
    cur = conn.cursor()

    try:

        #
        # count ALL requests in last minute
        #
        cur.execute(
            """
            SELECT COUNT(*) AS count
            FROM api_usage
            WHERE
                user_id=%s
                AND request_time >
                    NOW() - interval '1 minute'
            """,
            (user_id,)
        )

        result = cur.fetchone()

        request_count = result["count"]

        print(
            "\n========== RATE LIMIT =========="
        )

        print(
            "USER:",
            user_id
        )

        print(
            "REQUESTS LAST 60 SEC:",
            request_count
        )

        print(
            "CURRENT TIME:",
            datetime.now()
        )

        print(
            "================================\n"
        )

        #
        # allow first 30
        # block on 31st
        #
        effective_count = request_count + 1

        print("REQUESTS INCLUDING CURRENT:",effective_count)

        if effective_count > MAX_REQUESTS:
            block_user(
                user_id,
                api_key,
                ip_address,
                effective_count,
                "Request limit exceeded"
            )

            raise HTTPException(
                status_code=403,
                detail="Request limit exceeded"
            )

    finally:

        cur.close()
        conn.close()