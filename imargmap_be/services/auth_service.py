import secrets

from core.database import get_db1


from core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from core.validators import (
    is_business_email
)
from services.email_service import send_verification_email
from datetime import datetime, timedelta

def generate_api_key():
    return secrets.token_hex(32)

def generate_verification_token():
    return secrets.token_urlsafe(32)

def register_user(data):

   
    conn = get_db1()
    cur = conn.cursor()

    try:

        print("\n================ REGISTER =================")
        print("Email :", data.email)
        print("Phone :", data.phone_number)
        print("===========================================\n")

        if not is_business_email(data.email):
            return "business_email_required"

        # Existing user check
        cur.execute(
            """
            SELECT email, phone_number
            FROM users
            WHERE email=%s
               OR phone_number=%s
            """,
            (
                data.email,
                data.phone_number
            )
        )

        user = cur.fetchone()

        if user:

            if user["email"] == data.email:
                return "email_exists"

            if user["phone_number"] == data.phone_number:
                return "phone_exists"

        # Delete expired pending registrations
        cur.execute(
            """
            DELETE FROM pending_registrations
            WHERE token_expiry < NOW()
            """
        )

        token = generate_verification_token()
        expiry = datetime.utcnow() + timedelta(minutes=10)

        # Check pending registration for same email
        cur.execute(
            """
            SELECT id
            FROM pending_registrations
            WHERE email=%s
            """,
            (data.email,)
        )

        pending = cur.fetchone()

        print("Pending Row :", pending)

        if pending:

            print("Updating existing pending registration...")

            cur.execute(
                """
                UPDATE pending_registrations
                SET
                    full_name=%s,
                    phone_number=%s,
                    company_name=%s,
                    location=%s,
                    verification_token=%s,
                    token_expiry=%s,
                    email_verified=FALSE,
                    verified_at=NULL
                WHERE id=%s
                """,
                (
                    data.full_name,
                    data.phone_number,
                    data.company_name,
                    data.location,
                    token,
                    expiry,
                    pending["id"]
                )
            )

            print("Rows Updated :", cur.rowcount)

        else:

            print("Creating new pending registration...")

            cur.execute(
                """
                INSERT INTO pending_registrations
                (
                    full_name,
                    email,
                    phone_number,
                    company_name,
                    location,
                    verification_token,
                    token_expiry
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                RETURNING id
                """,
                (
                    data.full_name,
                    data.email,
                    data.phone_number,
                    data.company_name,
                    data.location,
                    token,
                    expiry
                )
            )

            inserted = cur.fetchone()

            print("Inserted ID :", inserted)

        conn.commit()

        cur.execute(
            """
            SELECT
                id,
                email,
                phone_number
            FROM pending_registrations
            ORDER BY id
            """
        )

        print("Pending Table :", cur.fetchall())

        send_verification_email(
            data.email,
            data.full_name,
            token
        )

        return "verification_sent"

    except Exception as e:

        conn.rollback()
        print("REGISTER ERROR:", e)
        raise

    finally:

        cur.close()
        conn.close()

def verify_registration_token(token):

    conn = get_db1()
    cur = conn.cursor()

    try:

        print("Received Token:", token)

        cur.execute(
            """
            SELECT
                id,
                email_verified,
                token_expiry
            FROM pending_registrations
            WHERE verification_token=%s
            """,
            (token,)
        )

        pending = cur.fetchone()

        print("Pending Record:", pending)

        if pending is None:
            print("Token not found")
            return "invalid"

        if pending["token_expiry"] < datetime.utcnow():
            print("Token expired")
            return "expired"

        if pending["email_verified"]:
            print("Already verified")
            return "already_verified"

        cur.execute(
            """
            UPDATE pending_registrations
            SET
                email_verified = TRUE,
                verified_at = NOW()
            WHERE id=%s
            """,
            (pending["id"],)
        )

        print("Rows Updated:", cur.rowcount)

        conn.commit()

        print("Database committed successfully.")

        return "verified"

    finally:
        cur.close()
        conn.close()

def create_account(token, password):

    conn = get_db1()
    cur = conn.cursor()
    print("================================")
    print("CREATE ACCOUNT TOKEN:", token)
    print("================================")
    try:

        cur.execute(
            """
            SELECT *
            FROM pending_registrations
            WHERE verification_token=%s
            """,
            (token,)
        )

        pending = cur.fetchone()

        if not pending:
            return "invalid"

        if pending["token_expiry"] < datetime.utcnow():
            return "expired"

        if not pending["email_verified"]:
            return "not_verified"

        hashed_password = hash_password(password)

        api_key = generate_api_key()

        cur.execute(
            """
            INSERT INTO users
            (
                email,
                password,
                full_name,
                phone_number,
                company_name,
                location,
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
                %s,
                %s,
                %s,
                'USER',
                'FREE',
                TRUE,
                %s
            )
            """,
            (
                pending["email"],
                hashed_password,
                pending["full_name"],
                pending["phone_number"],
                pending["company_name"],
                pending["location"],
                api_key
            )
        )

        cur.execute(
            """
            DELETE FROM pending_registrations
            WHERE id=%s
            """,
            (pending["id"],)
        )

        conn.commit()

        return True

    finally:

        cur.close()
        conn.close()

def login_user(data):

    
    conn = get_db1()
    cur = conn.cursor()


    try:

        cur.execute(
            """
            SELECT *
            FROM users
            WHERE email = %s
            """,
            (data.email,)
        )

        user = cur.fetchone()

        if not user:
            return None

        # User is blocked
        if not user["is_active"]:
            return "inactive"

        # API key revoked
        if user["api_key"] is None:
            return "api_key_revoked"

        # Invalid password
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
                "subscription": user["subscription_type"]
            }
        )

        return {
            "token": token,
            "api_key": user["api_key"]
        }

    finally:
        cur.close()
        conn.close()

def regenerate_api_key(user_id):

    conn = get_db1()
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
        conn.close()


def get_user_by_api_key(api_key):

    conn = get_db1()
    cur = conn.cursor()
    

    try:

        cur.execute(
            """
            SELECT *
            FROM users
            WHERE api_key=%s
            """,
            (api_key,)
        )

        return cur.fetchone()

    finally:
        cur.close()
        conn.close()
