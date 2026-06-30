'''from fastapi import APIRouter
from fastapi import Depends

from schemas.payment import PaymentRequest

from core.dependencies import get_current_user

from services.payment_service import (
    create_payment
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("")
def create_payment_api(
    data: PaymentRequest,
    user=Depends(get_current_user)
):

    payment = create_payment(
        user["user_id"],
        data.amount,
        f"TXN_{user['user_id']}"
    )

    return {
        "success": True,
        "message": "Payment successful. Premium activated.",
        "payment_id": payment["id"]
    }'''
from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request

from core.dependencies import get_current_user

from schemas.payment import (
    CreatePaymentRequest,
    VerifyPaymentRequest
)

from services.payment_service import (
    create_payment,
    verify_payment,
    get_payment_status,
    get_payment_history
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


#
# Create Payment Order
#
@router.post("")
def create_payment_api(
        data: CreatePaymentRequest,
        request: Request,
        user=Depends(get_current_user)
):

    '''payment = create_payment(
        user_id=user["user_id"],
        email=user["email"],
        api_key=user["api_key"],
        ip_address=request.client.host,
        plan_name=data.plan_name,
        duration_type=data.duration_type
    )'''

    payment = create_payment(
    user_id=user["user_id"],
    email=user["email"],
    plan_name=data.plan_name,
    duration_type=data.duration_type
    )
    return {
        "success": True,
        "order_id": payment["order_id"],
        "payment_id": payment["payment_id"]
    }


#
# Verify Payment
#
@router.post("/verify-payment")
def verify_payment_api(
        data: VerifyPaymentRequest
):

    result = verify_payment(
        order_id=data.order_id,
        transaction_id=data.transaction_id,
        gateway_name=data.gateway_name,
        payment_success=data.payment_success
    
    )
    

    return {
        "success": True,
        "payment_status": result["payment_status"],
        "order_id": result["order_id"]
    }


#
# Get Payment Status
#
#@router.get("/status/{order_id}")
@router.get("/status/{order_id}")
def payment_status_api(
        order_id: str
):

    payment = get_payment_status(
        order_id
    )
    

    return {
        "success": True,
        "payment": payment
    }


#
# Payment History
#
@router.get("/history")
def payment_history_api(
        user=Depends(get_current_user)
):

    history = get_payment_history(
        user["user_id"]
    )

    return {
        "success": True,
        "payments": history
    }