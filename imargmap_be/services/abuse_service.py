from fastapi import HTTPException

#from core.database import admin_test
from core.database import get_db1




def block_user(
        user_id,
        api_key,
        ip_address,
        request_count,
        reason
):

    
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
                detail="Request Limit Exceeded"
            )

    finally:

        cur.close()
        conn.close()
