from core.database import get_db1


def get_all_users():

    conn = get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT
        u.*,

        COUNT(a.id) AS request_count,

        COALESCE(
            STRING_AGG(
                DISTINCT a.ip_address,
                ', '
            ),
            ''
        ) AS ip_addresses

    FROM users u

    LEFT JOIN api_usage a
        ON u.id = a.user_id

    GROUP BY u.id

    ORDER BY u.id DESC
            """
        )

        return cur.fetchall()

    finally:
        cur.close()
        conn.close()

def update_subscription(
    user_id,
    subscription_type,
    subscription_expiry=None
):

    conn = get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            UPDATE users
            SET
                subscription_type=%s,
                subscription_expiry=%s
            WHERE id=%s
            """,
            (
                subscription_type,
                subscription_expiry,
                user_id
            )
        )

        conn.commit()

        return True

    finally:
        cur.close()
        conn.close()

def update_role(
    user_id,
    role
):

    conn = get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            UPDATE users
            SET role=%s
            WHERE id=%s
            """,
            (
                role,
                user_id
            )
        )

        conn.commit()

        return True

    finally:
        cur.close()
        conn.close()

def activate_user(user_id):
    conn = get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            UPDATE users
            SET is_active = TRUE
            WHERE id = %s
            """,
            (user_id,)
        )
        #newly added
        cur.execute(
            """
            UPDATE blocked_ips
            SET is_active=FALSE
            WHERE ip_address IN
            (
                SELECT DISTINCT ip_address 
                FROM abuse_logs
                WHERE user_id=%s
            )
            """,
            (user_id,)
        )

        conn.commit()

        return True

    finally:
        cur.close()
        conn.close()

def deactivate_user(user_id):
    conn = get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            UPDATE users
            SET
                is_active = FALSE,
                api_key = NULL
            WHERE id = %s
            """,
            (user_id,)
        )

        conn.commit()

        return True

    finally:
        cur.close()
        conn.close()

def delete_user(user_id):
    conn = get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            DELETE FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        conn.commit()

        return True

    finally:
        cur.close()
        conn.close()

def get_dashboard_stats():
    conn = get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT
                COUNT(*) AS total_users,

                COUNT(*) FILTER (
                    WHERE subscription_type = 'PREMIUM'
                ) AS premium_users,

                COUNT(*) FILTER (
                    WHERE subscription_type = 'FREE'
                ) AS free_users,

                COUNT(*) FILTER (
                    WHERE is_active = TRUE
                ) AS active_users,

                COUNT(*) FILTER (
                    WHERE is_active = FALSE
                ) AS inactive_users

            FROM users
            """
        )

        return cur.fetchone()

    finally:
        cur.close()
        conn.close()
#IP and admin related
def get_blocked_ips():

    conn = get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT 
                ip_address,
                blocked_reason,
                blocked_at,
                is_active
            FROM blocked_ips
            WHERE is_active=TRUE
            ORDER BY blocked_at DESC
            """
        )

        return cur.fetchall()

    finally:

        cur.close()
        conn.close()
def unblock_ip(ip_address):

    conn = get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            UPDATE blocked_ips
            SET is_active=FALSE
            WHERE ip_address=%s
            """,
            (ip_address,)
        )

        conn.commit()

        return True

    finally:

        cur.close()
        conn.close()

#IP USED BY USER
def get_user_ips():

    conn = get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT
                u.id,
                STRING_AGG(
                    DISTINCT a.ip_address,
                    ', '
                ) AS ip_addresses

            FROM users u

            LEFT JOIN api_usage a
                ON u.id = a.user_id

            GROUP BY u.id
            """
        )

        rows = cur.fetchall()

        return {
            row["id"]: row["ip_addresses"]
            for row in rows
        }

    finally:
        cur.close()
        conn.close()