import secrets

#from core.database import get_db1
#from core.database import get_aoi_db
from core.database import admin_test
from core.security import (
    hash_password,
    verify_password,
    create_access_token
)


def generate_api_key():
    return secrets.token_hex(32)


def register_user(data):

    # = get_db1()
    #conn = get_aoi_db()
    conn = admin_test()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT id
            FROM users
            WHERE email=%s
            """,
            (data.email,)
        )

        if cur.fetchone():
            return None

        hashed_password = hash_password(
            data.password
        )

        api_key = generate_api_key()

        cur.execute(
            """
            INSERT INTO users
            (
                email,
                password,
                full_name,
                role,
                subscription_type,
                is_active,
                api_key
            )
            VALUES
            (
                %s,
                %s,
                %s,
                'USER',
                'FREE',
                TRUE,
                %s
            )
            RETURNING
                id,
                email,
                full_name,
                api_key
            """,
            (
                data.email,
                hashed_password,
                data.full_name,
                api_key
            )
        )

        user = cur.fetchone()

        conn.commit()

        return user

    finally:
        cur.close()
        conn.close()


def login_user(data):

    #conn = get_db1()
    #conn = get_aoi_db()
    #cur = conn.cursor()
    conn = admin_test()
    cur = conn.cursor()


    try:

        cur.execute(
            """
            SELECT *
            FROM users
            WHERE email=%s
            """,
            (data.email,)
        )

        user = cur.fetchone()

        if not user:
            return None

        if not user["is_active"]:
            return "inactive"

        if not verify_password(
            data.password,
            user["password"]
        ):
            return False

        token = create_access_token(
            {
                "user_id": user["id"],
                "email": user["email"],
                "role": user["role"],
                "subscription": user["subscription_type"],
                "api_key": user["api_key"]
            }
        )

        return {
            "token": token,
            "api_key": user["api_key"],
            "user": {
                "id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"],
                "role": user["role"],
                "subscription_type": user["subscription_type"],
                "is_active": user["is_active"]
            }
        }

    finally:
        cur.close()
        conn.close()


'''def regenerate_api_key(user_id):

    #conn = get_db1()
    #cur = conn.cursor()
    conn = admin_test()
    cur = conn.cursor()


    try:

        new_api_key = generate_api_key()

        cur.execute(
            """
            UPDATE users
            SET api_key=%s
            WHERE id=%s
            RETURNING api_key
            """,
            (
                new_api_key,
                user_id
            )
        )

        result = cur.fetchone()

        conn.commit()

        return result

    finally:
        cur.close()
        conn.close()'''
def regenerate_api_key(user_id):

    conn = admin_test()
    cur = conn.cursor()

    try:

        new_api_key = generate_api_key()

        cur.execute(
            """
            UPDATE users
            SET
                api_key=%s,
                is_active=TRUE
            WHERE id=%s
            RETURNING api_key
            """,
            (
                new_api_key,
                user_id
            )
        )

        result = cur.fetchone()

        conn.commit()

        return result

    finally:
        cur.close()
        conn.close()


def get_user_by_api_key(api_key):

    #conn = get_db1()
    #cur = conn.cursor()
    conn = admin_test()
    cur = conn.cursor()


    try:

        cur.execute(
            """
            SELECT *
            FROM users
            WHERE api_key=%s
            """
            ,
            (api_key,)
        )

        return cur.fetchone()

    finally:
        cur.close()
        conn.close()