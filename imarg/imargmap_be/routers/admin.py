from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from core.dependencies import get_current_user

from services.admin_service import (
get_all_users,
update_subscription,
update_role,
activate_user,
deactivate_user,
delete_user,
get_dashboard_stats,
get_blocked_ips,
unblock_ip
)

router = APIRouter(
prefix="/admin",
tags=["Admin"]
)

def check_admin(user):
    if user["role"] != "ADMIN":

        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )


@router.get("/users")
def list_users(
    user=Depends(get_current_user)
    ):


    check_admin(user)

    return {
        "success": True,
        "data": get_all_users()
    }


@router.put("/users/{user_id}/subscription")
def change_subscription(
    user_id: int,
    subscription_type: str,
    subscription_expiry: str = None,
    user=Depends(get_current_user)
    ):


    check_admin(user)

    update_subscription(
        user_id,
        subscription_type,
        subscription_expiry
    )

    return {
        "success": True,
        "message": "Subscription updated successfully"
    }


@router.put("/users/{user_id}/role")
def change_role(
    user_id: int,
    role: str,
    user=Depends(get_current_user)
    ):


    check_admin(user)

    update_role(
        user_id,
        role
    )

    return {
        "success": True,
        "message": "Role updated successfully"
    }


@router.put("/users/{user_id}/activate")
def activate(
    user_id: int,
    user=Depends(get_current_user)
    ):


    check_admin(user)

    activate_user(user_id)

    return {
        "success": True,
        "message": "User activated successfully"
    }


@router.put("/users/{user_id}/deactivate")
def deactivate(
    user_id: int,
    user=Depends(get_current_user)
    ):


    check_admin(user)

    deactivate_user(user_id)

    return {
        "success": True,
        "message": "User deactivated successfully"
    }


@router.delete("/users/{user_id}")
def remove_user(
    user_id: int,
    user=Depends(get_current_user)
    ):

    check_admin(user)

    delete_user(user_id)

    return {
        "success": True,
        "message": "User deleted successfully"
    }


@router.get("/dashboard")
def dashboard(user=Depends(get_current_user)):

    check_admin(user)

    stats = get_dashboard_stats()

    return {
        "success": True,
        "data": stats
    }
@router.get("/blocked-ips")
def blocked_ips(
    user=Depends(get_current_user)
):

    check_admin(user)

    return {
        "success": True,
        "data": get_blocked_ips()
    }
@router.put("/unblock-ip/{ip_address}")
def unblock_ip_api(
    ip_address: str,
    user=Depends(get_current_user)
):

    check_admin(user)

    unblock_ip(ip_address)

    return {
        "success": True,
        "message": "IP unblocked successfully"
    }
