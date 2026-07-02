from core.database import get_db1


import secrets

#from core.database import get_aoi_db

def get_user_profile(user_id):

    conn = get_db1()
    
    cur = conn.cursor()


    try:

        cur.execute(
            """
            SELECT 
                id,
                full_name,
                email,
                role,
                subscription_type,
                api_key,
                is_active,
                created_at
            FROM users
            WHERE id = %s
            """,
            (user_id,)
        )

        return cur.fetchone()

    finally:
        cur.close()
        conn.close()


def update_profile(
    user_id,
    full_name
):

    conn = get_db1()
    cur = conn.cursor()
    

    try:

        cur.execute(
            """
            UPDATE users
            SET full_name = %s
            WHERE id = %s
            """,
            (
                full_name,
                user_id
            )
        )

        conn.commit()

        return True

    finally:
        cur.close()
        conn.close()


