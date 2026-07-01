from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)
from fastapi.responses import HTMLResponse

from core.database import get_db1
from core.dependencies import get_current_user

from schemas.auth import (
    RegisterRequest,
    LoginRequest,
    CreateAccountRequest
)

from services.auth_service import (
    register_user,
    login_user,
    regenerate_api_key,
    verify_registration_token,
    create_account
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


# ----------------------------------------------------
# Register
# ----------------------------------------------------
@router.post("/register")
def register(data: RegisterRequest):

    result = register_user(data)

    if result == "business_email_required":
        raise HTTPException(
            status_code=400,
            detail="Please use a business email address."
        )

    if result == "email_exists":
        raise HTTPException(
            status_code=400,
            detail="Email address is already registered."
        )

    if result == "phone_exists":
        raise HTTPException(
            status_code=400,
            detail="Mobile number is already registered."
        )

    return {
        "success": True,
        "message": "Verification email sent successfully."
    }


# ----------------------------------------------------
# Verify Email
# ----------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
SUCCESS_TEMPLATE = BASE_DIR / "templates" / "verify_success.html"


def render_verify_page(title, message, icon):

    with open(SUCCESS_TEMPLATE, "r", encoding="utf-8") as file:
        html = file.read()

    html = html.replace("{{title}}", title)
    html = html.replace("{{message}}", message)
    html = html.replace("{{icon}}", icon)

    return HTMLResponse(html)


BASE_DIR = Path(__file__).resolve().parent.parent
SUCCESS_TEMPLATE = BASE_DIR / "templates" / "verify_success.html"


def render_verify_page(title, message, icon):

    with open(
        SUCCESS_TEMPLATE,
        "r",
        encoding="utf-8"
    ) as file:

        html = file.read()

    html = html.replace("{{title}}", title)
    html = html.replace("{{message}}", message)
    html = html.replace("{{icon}}", icon)

    return HTMLResponse(content=html)


@router.get("/verify-email", response_class=HTMLResponse)
def verify_email(token: str):

    print("===== VERIFY ROUTE CALLED =====")
    print("Token:", token)

    result = verify_registration_token(token)

    print("Result:", result)

    if result == "verified":
        return render_verify_page(
            "Email Verified Successfully",
            "Your email address has been successfully verified. You may now return to the application and continue creating your account.",
            "✔"
        )

    elif result == "already_verified":
        return render_verify_page(
            "Already Verified",
            "Your email address has already been verified.",
            "ℹ"
        )

    elif result == "expired":
        return render_verify_page(
            "Verification Link Expired",
            "Your verification link has expired. Please register again.",
            "✖"
        )

    return render_verify_page(
        "Invalid Verification Link",
        "The verification link is invalid.",
        "✖"
    )

# ----------------------------------------------------
# Email Status
# ----------------------------------------------------
@router.get("/email-status")
def email_status(email: str):

    conn = get_db1()
    cur = conn.cursor()

    try:

        cur.execute(
            """
            SELECT email_verified
            FROM pending_registrations
            WHERE email=%s
            """,
            (email,)
        )

        row = cur.fetchone()

        if not row:
            raise HTTPException(
                status_code=404,
                detail="Email not found."
            )

        return {
            "success": True,
            "verified": row["email_verified"]
        }

    finally:

        cur.close()
        conn.close()


# ----------------------------------------------------
# Create Account
# ----------------------------------------------------
@router.post("/create-account")
def create_user_account(data: CreateAccountRequest):

    result = create_account(
        data.token,
        data.password
    )

    if result == "invalid":
        raise HTTPException(
            status_code=400,
            detail="Invalid verification link."
        )

    if result == "expired":
        raise HTTPException(
            status_code=400,
            detail="Verification link has expired."
        )

    if result == "not_verified":
        raise HTTPException(
            status_code=400,
            detail="Please verify your email first."
        )

    return {
        "success": True,
        "message": "Account created successfully."
    }


# ----------------------------------------------------
# Login
# ----------------------------------------------------
@router.post("/login")
def login(data: LoginRequest):

    result = login_user(data)

    if result is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if result == "inactive":
        raise HTTPException(
            status_code=403,
            detail="Your account has been blocked. Please contact the administrator."
        )

    if result == "api_key_revoked":
        raise HTTPException(
            status_code=403,
            detail="Your API key has been revoked. Please contact the administrator."
        )

    if result is False:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    return {
        "success": True,
        "message": "Login successful.",
        "token": result["token"],
        "api_key": result["api_key"]
    }


# ----------------------------------------------------
# Regenerate API Key
# ----------------------------------------------------
@router.post("/users/{user_id}/regenerate-api-key")
def regenerate_user_api_key(
    user_id: int,
    user=Depends(get_current_user)
):

    check_admin(user)

    result = regenerate_api_key(user_id)

    return {
        "success": True,
        "message": "API key regenerated successfully.",
        "api_key": result["api_key"]
    }