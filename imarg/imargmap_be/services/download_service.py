#from core.database import get_db1
#from core.database import get_aoi_db
from core.database import admin_test

def can_download(
    user_id
):

    #conn = get_db1()
    #conn = get_aoi_db()
    conn = admin_test()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT COUNT(*)
            FROM payments
            WHERE user_id=%s
            AND payment_status='SUCCESS'
            """,
            (user_id,)
        )

        result = cur.fetchone()

        return result["count"] > 0

    finally:
        cur.close()
        conn.close()