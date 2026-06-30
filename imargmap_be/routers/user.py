'''from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from core.dependencies import (
    get_current_user
)
from core.dependencies import (
    get_current_user,
    admin_required
)

from services.user_service import (
    get_user_profile
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
#newly added
from services.user_service import (
    get_user_profile,
    block_user,
    unblock_user,
    get_all_users
)

from services.auth_service import regenerate_api_key

@router.get("/profile")
def profile(
    user=Depends(get_current_user)
):
    profile = get_user_profile(
        user["user_id"]
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "success": True,
        "data": {
            "full_name": profile["full_name"],
            "email": profile["email"],
            "subscription_type": profile["subscription_type"],
            "api_key": profile["api_key"]
        }
    }


@router.get("/dashboard")
def dashboard(
    user=Depends(get_current_user)
):
    profile = get_user_profile(
        user["user_id"]
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "success": True,
        "data": {
            "id": profile["id"],
            "full_name": profile["full_name"],
            "email": profile["email"],
            "role": profile["role"],
            "subscription_type": profile["subscription_type"],
            "api_key": profile["api_key"],
            "is_active": profile["is_active"],
            "created_at": profile["created_at"]
        }
    }
#newly added
@router.put("/admin/regenerate-api-key/{user_id}")
@router.put("/admin/block/{user_id}")
def block_user_api(
    user_id: int,
    admin=Depends(admin_required)
):

    result = regenerate_api_key(user_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "success": True,
        "api_key": result["api_key"]
    }
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request
)

from core.dependencies import (
    get_current_user,
    admin_required
)

from services.audit_service import log_api_usage
from services.abuse_service import check_abuse

from services.user_service import (
    get_user_profile,
    get_all_users,
    block_user,
    unblock_user
)

from services.auth_service import (
    regenerate_api_key
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/profile")
def profile(
    request: Request,
    user=Depends(get_current_user)
):

    ip_address = request.client.host

    # Log request
    log_api_usage(
        user["user_id"],
        user["api_key"],
        ip_address,
        "/users/profile"
    )

    # Check abuse
    check_abuse(
        user["user_id"],
        user["api_key"],
        ip_address
    )

    profile = get_user_profile(
        user["user_id"]
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "success": True,
        "data": {
            "full_name": profile["full_name"],
            "email": profile["email"],
            "subscription_type": profile["subscription_type"],
            "api_key": profile["api_key"]
        }
    }


@router.get("/dashboard")
def dashboard(
    request: Request,
    user=Depends(get_current_user)
):

    ip_address = request.client.host

    log_api_usage(
        user["user_id"],
        user["api_key"],
        ip_address,
        "/users/dashboard"
    )

    check_abuse(
        user["user_id"],
        user["api_key"],
        ip_address
    )

    profile = get_user_profile(
        user["user_id"]
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "success": True,
        "data": {
            "id": profile["id"],
            "full_name": profile["full_name"],
            "email": profile["email"],
            "role": profile["role"],
            "subscription_type": profile["subscription_type"],
            "api_key": profile["api_key"],
            "is_active": profile["is_active"],
            "created_at": profile["created_at"]
        }
    }


# ADMIN APIs

@router.get("/admin/users")
def get_users(
    admin=Depends(admin_required)
):

    users = get_all_users()

    return {
        "success": True,
        "users": users
    }


@router.put("/admin/block/{user_id}")
def block_user_api(
    user_id: int,
    admin=Depends(admin_required)
):

    user = block_user(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "success": True,
        "message": "User blocked successfully"
    }


@router.put("/admin/unblock/{user_id}")
def unblock_user_api(
    user_id: int,
    admin=Depends(admin_required)
):

    user = unblock_user(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "success": True,
        "message": "User unblocked successfully"
    }


@router.put("/admin/regenerate-api-key/{user_id}")
def regenerate_api_key_api(
    user_id: int,
    admin=Depends(admin_required)
):

    result = regenerate_api_key(
        user_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "success": True,
        "message": "API key regenerated successfully",
        "api_key": result["api_key"]
    }'''
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request
)

from core.dependencies import (
    get_current_user
    #admin_required                         #own req
)

'''from services.user_service import (
    get_user_profile,
    get_all_users,
    block_user,
    unblock_user
)'''

'''from services.auth_service import (
    regenerate_api_key
)'''

from services.audit_service import log_api_usage
from services.abuse_service import check_abuse


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



# USER PROFILE

@router.get("/profile")
def profile(
    request: Request,
    user=Depends(get_current_user)
):

    profile = get_user_profile(
        user["user_id"]
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    ip_address = request.client.host

    log_api_usage(
        user["user_id"],
        user["api_key"],
        ip_address,
        "/users/profile"
    )

    check_abuse(
        user["user_id"],
        user["api_key"],
        ip_address
    )

    return {
        "success": True,
        "data": {
            "full_name": profile["full_name"],
            "email": profile["email"],
            "subscription_type": profile["subscription_type"],
            "api_key": profile["api_key"]
        }
    }



# USER DASHBOARD


@router.get("/dashboard")
def dashboard(
    request: Request,
    user=Depends(get_current_user)
):

    profile = get_user_profile(
        user["user_id"]
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    ip_address = request.client.host

    log_api_usage(
        user["user_id"],
        user["api_key"],
        ip_address,
        "/users/dashboard"
    )

    check_abuse(
        user["user_id"],
        user["api_key"],
        ip_address
    )

    return {
        "success": True,
        "data": {
            "id": profile["id"],
            "full_name": profile["full_name"],
            "email": profile["email"],
            "role": profile["role"],
            "subscription_type": profile["subscription_type"],
            "api_key": profile["api_key"],
            "is_active": profile["is_active"],
            "created_at": profile["created_at"]
        }
    }



# ADMIN - GET USERS


'''@router.get("/admin/users")
def get_users(
    request: Request,
    admin=Depends(admin_required)
):

    ip_address = request.client.host

    log_api_usage(
        admin["user_id"],
        admin["api_key"],
        ip_address,
        "/users/admin/users"
    )

    check_abuse(
        admin["user_id"],
        admin["api_key"],
        ip_address
    )

    users = get_all_users()

    return {
        "success": True,
        "users": users
    }



# ADMIN - BLOCK USER


@router.put("/admin/block/{user_id}")
def block_user_api(
    user_id: int,
    request: Request,
    admin=Depends(admin_required)
):

    ip_address = request.client.host

    log_api_usage(
        admin["user_id"],
        admin["api_key"],
        ip_address,
        "/users/admin/block"
    )

    check_abuse(
        admin["user_id"],
        admin["api_key"],
        ip_address
    )

    user = block_user(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "success": True,
        "message": "User blocked successfully"
    }



# ADMIN - UNBLOCK USER


@router.put("/admin/unblock/{user_id}")
def unblock_user_api(
    user_id: int,
    request: Request,
    admin=Depends(admin_required)
):

    ip_address = request.client.host

    log_api_usage(
        admin["user_id"],
        admin["api_key"],
        ip_address,
        "/users/admin/unblock"
    )

    check_abuse(
        admin["user_id"],
        admin["api_key"],
        ip_address
    )

    user = unblock_user(user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "success": True,
        "message": "User unblocked successfully"
    }



# ADMIN - REGENERATE API KEY


@router.put("/admin/regenerate-api-key/{user_id}")
def regenerate_api_key_api(
    user_id: int,
    request: Request,
    admin=Depends(admin_required)
):

    ip_address = request.client.host

    log_api_usage(
        admin["user_id"],
        admin["api_key"],
        ip_address,
        "/users/admin/regenerate-api-key"
    )

    check_abuse(
        admin["user_id"],
        admin["api_key"],
        ip_address
    )

    result = regenerate_api_key(
        user_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "success": True,
        "message": "API key regenerated successfully",
        "api_key": result["api_key"]
    }'''