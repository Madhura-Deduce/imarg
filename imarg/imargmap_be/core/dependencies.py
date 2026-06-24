from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer

from jose import jwt
from jose import JWTError

from core.config import (
    SECRET_KEY,
    ALGORITHM
)

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

        return payload

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
#newly added
def admin_required(
    user=Depends(get_current_user)
):

    if user["role"] != "ADMIN":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user