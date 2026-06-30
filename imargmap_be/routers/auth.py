from fastapi import APIRouter, HTTPException
from fastapi import Depends
from core.dependencies import get_current_user

from schemas.auth import (
    RegisterRequest,
    LoginRequest
)

from services.auth_service import (
    register_user,
    login_user,
    regenerate_api_key
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

def check_admin(user):
    if user["role"] != "ADMIN":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

@router.post("/register")
def register(data: RegisterRequest):

    result = register_user(data)

    if result == "email_exists":

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    if result == "phone_exists":

        raise HTTPException(
            status_code=400,
            detail="Mobile number already registered"
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
        "message": "Login successful",
        "token": result["token"],
        "api_key": result["api_key"],
        "user": result["user"]
    }

@router.post("/users/{user_id}/regenerate-api-key")
def regenerate_user_api_key(
    user_id: int,
    user=Depends(get_current_user)
):

    check_admin(user)

    result = regenerate_api_key(
        user_id
    )

    return {
        "success": True,
        "message": "API key regenerated successfully",
        "api_key": result["api_key"]
    }