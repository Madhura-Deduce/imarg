from fastapi import HTTPException

#from core.database import admin_test
from core.database import get_db1


'''from core.config import (
    #USER_REQUEST_LIMIT,
    #API_KEY_REQUEST_LIMIT,
    #IP_REQUEST_LIMIT,
    #RATE_WINDOW_MINUTES,
    #MAX_IPS_PER_USER,
    #IP_ROTATION_WINDOW_MINUTES,
    #GLOBAL_REQUEST_LIMIT
)'''


def block_user(
        user_id,
        api_key,
        ip_address,
        request_count,
        reason
):

    #conn = admin_test()
    conn=get_db1()
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
        print("absue called")
        # Store blocked IP

        cur.execute(
            """
            INSERT INTO blocked_ips
            (
                ip_address,
                blocked_reason,
                is_active
            )
            VALUES
            (
                %s,
                %s,
                TRUE
            )
            ON CONFLICT (ip_address)
            DO UPDATE
            SET
                blocked_reason = EXCLUDED.blocked_reason,
                blocked_at = NOW(),
                is_active = TRUE
            """,
            (
                ip_address,
                reason
            )
        )

        # Block user
        cur.execute(
            """
            UPDATE users
            SET
                is_active = FALSE,
                
                api_key = NULL,
                blocked_at=NOW(),
                blocked_reason=%s
            WHERE id=%s
            """,
            (reason,user_id)
        )
        print(
        "BLOCKING USER:",
        user_id,
        "COUNT:",
        request_count,
        "IP:",
        ip_address
        )
         
        cur.execute(
            """
            DELETE 
            FROM user_request_counter
            where USER_ID=%s
            """,
            (user_id,)
         )

        conn.commit()

    finally:

        cur.close()
        conn.close()

#("check abuse")
'''def check_abuse(
        user_id,
        api_key,
        ip_address
):

    #conn = admin_test()
    if is_ip_blocked(ip_address):
        raise HTTPException(
            status_code=403,
            detail="IP_BLOCKED"
        )
    conn=get_db1()

    cur = conn.cursor()

    try:

        
        # USER LIMIT
        
        cur.execute(
            f"""
            SELECT COUNT(*)
            FROM api_usage
            WHERE user_id=%s
            AND request_time >
            NOW() - interval '{RATE_WINDOW_MINUTES} minute'
            """,
            (user_id,)
        )

        user_count = cur.fetchone()["count"]

        if user_count > GLOBAL_REQUEST_LIMIT:

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
            FROM api_usage
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
            FROM api_usage
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
            FROM api_usage
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
        conn.close()'''
def is_ip_blocked(ip_address):

    conn = get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT id
            FROM blocked_ips
            WHERE
                ip_address=%s
                AND is_active=TRUE
            """,
            (ip_address,)
        )

        result = cur.fetchone()

        return result is not None

    finally:

        cur.close()
        conn.close()
'''from fastapi import HTTPException

from core.database import get_db1

from core.config import (
    GLOBAL_REQUEST_LIMIT,
    RATE_WINDOW_MINUTES
)


def block_user(
        user_id,
        api_key,
        ip_address,
        request_count,
        reason
):

    conn = get_db1()
    cur = conn.cursor()

    try:

        #
        # Store abuse history
        #
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
                %s,
                %s,
                %s,
                %s,
                %s
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

        #
        # Store blocked IP
        #
        cur.execute(
            """
            INSERT INTO blocked_ips
            (
                ip_address,
                blocked_reason,
                is_active
            )
            VALUES
            (
                %s,
                %s,
                TRUE
            )
            ON CONFLICT (ip_address)
            DO UPDATE
            SET
                blocked_reason = EXCLUDED.blocked_reason,
                blocked_at = NOW(),
                is_active = TRUE
            """,
            (
                ip_address,
                reason
            )
        )

        #
        # Block user
        #
        cur.execute(
            """
            UPDATE users
            SET
                is_active = FALSE,
                api_key = NULL,
                blocked_at = NOW(),
                blocked_reason = %s
            WHERE id = %s
            """,
            (
                reason,
                user_id
            )
        )

        conn.commit()

    finally:

        cur.close()
        conn.close()


def is_ip_blocked(ip_address):

    conn = get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT id
            FROM blocked_ips
            WHERE
                ip_address=%s
                AND is_active=TRUE
            """,
            (ip_address,)
        )

        result = cur.fetchone()

        return result is not None

    finally:

        cur.close()
        conn.close()'''


def check_abuse(
        user_id,
        api_key,
        ip_address
):

    #
    # Check whether IP already blocked
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
        # Count ALL requests made by this user
        # within configured window
        #
        cur.execute(
            f"""
            SELECT COUNT(*) AS count
            FROM api_usage
            WHERE
                user_id=%s
                AND request_time >
                    NOW() - (%s * interval '1 minute')
            """,
            (user_id,)
        )

        result = cur.fetchone()

        global_count = result["count"]

        print(
            "user:",
            user_id,
            "requests:",
            global_count
        )

        #
        # Block if limit exceeded
        #
        if global_count >= GLOBAL_REQUEST_LIMIT:

            block_user(
                user_id,
                api_key,
                ip_address,
                global_count,
                "GLOBAL_REQUEST_LIMIT_EXCEEDED"
            )

            raise HTTPException(
                status_code=403,
                detail="GLOBAL_REQUEST_LIMIT_EXCEEDED"
            )

    finally:

        cur.close()
        conn.close()
'''def check_abuse(
        user_id,
        api_key,
        ip_address
):

    #
    # Check if IP already blocked
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
        # Force latest committed rows
        #
        conn.commit()

        #
        # Count all requests for this user
        #
        cur.execute(
            f"""
            SELECT COUNT(*) AS count
            FROM api_usage
            WHERE user_id = %s
            AND request_time >=
                NOW() - interval '{RATE_WINDOW_MINUTES} minute'
            """,
            (user_id,)
        )

        result = cur.fetchone()

        global_count = result["count"]

        print(
            f"user: {user_id} requests: {global_count}"
        )

        #
        # Block when limit reached
        #
        if global_count >= GLOBAL_REQUEST_LIMIT:

            print(
                f"BLOCKING USER {user_id}"
            )

            block_user(
                user_id=user_id,
                api_key=api_key,
                ip_address=ip_address,
                request_count=global_count,
                reason="GLOBAL_REQUEST_LIMIT_EXCEEDED"
            )

            raise HTTPException(
                status_code=403,
                detail="GLOBAL_REQUEST_LIMIT_EXCEEDED"
            )

        return global_count

    finally:

        cur.close()
        conn.close()'''