from datetime import datetime, timezone

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer

from jose import jwt
from jose import JWTError
from services.abuse_service import is_ip_blocked


from core.config import (
    SECRET_KEY,
    ALGORITHM
)

from core.database import get_db1

security = HTTPBearer()


def get_current_user(
    token=Depends(security)
):

    try:

        payload = jwt.decode(
            token.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload["user_id"]

        conn = get_db1()
        cur = conn.cursor()

        try:

            cur.execute(
                """
                SELECT *
                FROM users
                WHERE id = %s
                """,
                (user_id,)
            )

            user = cur.fetchone()

            if not user:

                raise HTTPException(
                    status_code=401,
                    detail="User not found"
                )
            if not user["is_active"]:
                raise HTTPException(
                    status_code=403,
                    detail="Your account has been blocked."
                )

            if user["api_key"] is None:
                raise HTTPException(
                    status_code=401,
                    detail="API Key has been revoked."
                )

            # Auto downgrade expired premium users
            if (
                user["subscription_type"] == "PREMIUM"
                and user["subscription_expiry"] is not None
                and user["subscription_expiry"] <= datetime.now()
            ):

                cur.execute(
                    """
                    UPDATE users
                    SET subscription_type = 'FREE'
                    WHERE id = %s
                    """,
                    (user_id,)
                )

                conn.commit()

                user["subscription_type"] = "FREE"

            return {
                "user_id": user["id"],
                "email": user["email"],
                "role": user["role"],
                "subscription": user["subscription_type"],
                "api_key": user["api_key"]
            }

        finally:

            cur.close()
            conn.close()

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
