from fastapi import APIRouter, HTTPException

from schemas.auth import (
    RegisterRequest,
    LoginRequest
)

from services.auth_service import (
    register_user,
    login_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(data: RegisterRequest):

    result = register_user(data)

    if result is None:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    return {
        "success": True,
        "message": "Registration successful",
        "api_key": result["api_key"]
    }


@router.post("/login")
def login(data: LoginRequest):

    result = login_user(data)

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    if result == "inactive":
        raise HTTPException(
            status_code=403,
            detail="User account inactive"
        )

    if result is False:
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    return {
        "success": True,
        "token": result["token"],
        "user": {
            "id": result["user"]["id"],
            "email": result["user"]["email"],
            "full_name": result["user"]["full_name"],
            "role": result["user"]["role"],
            "subscription": result["user"]["subscription_type"],
        }
    }