#from core.database import get_db1
#from core.database import get_aoi_db
from core.database import admin_test
import secrets

#from core.database import get_aoi_db

def get_user_profile(user_id):

    #conn = get_db1()
    #conn = get_aoi_db()
    # = conn.cursor()
    conn = admin_test()
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
            WHERE id=%s
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

    '''conn = get_db1()
    cur = conn.cursor()'''
    conn = admin_test()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            UPDATE users
            SET full_name=%s
            WHERE id=%s
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


def get_all_users():

    '''conn = get_db1()
    cur = conn.cursor()'''
    conn = admin_test()
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
                is_active
            FROM users
            ORDER BY id DESC
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

    '''conn = get_db1()
    cur = conn.cursor()'''

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

    '''conn = get_db1()
    cur = conn.cursor()'''
    conn = admin_test()
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
#new functions
def generate_api_key():
    return secrets.token_hex(32)
def block_user(user_id):

    '''conn = get_aoi_db()
    cur = conn.cursor()'''
    conn = admin_test()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            UPDATE users
            SET
                is_active = FALSE,
                api_key = NULL
            WHERE id=%s
            RETURNING id
            """,
            (user_id,)
        )

        user = cur.fetchone()

        conn.commit()

        return user

    finally:
        cur.close()
        conn.close()
def unblock_user(user_id):

    '''conn = get_aoi_db()
    cur = conn.cursor()'''
    conn = admin_test()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            UPDATE users
            SET is_active = TRUE
            WHERE id=%s
            RETURNING id
            """,
            (user_id,)
        )

        user = cur.fetchone()

        conn.commit()

        return user

    finally:
        cur.close()
        conn.close()
