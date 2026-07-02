import re
import phonenumbers

PUBLIC_EMAIL_DOMAINS = {
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "outlook.com",
    "icloud.com",
    "aol.com",
    "proton.me",
}

EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"


def is_valid_email(email: str) -> bool:
    """
    Validate email format.
    """
    return bool(re.match(EMAIL_REGEX, email))


def is_business_email(email: str) -> bool:
    """
    Allow only business email addresses.
    """
    try:
        domain = email.split("@")[1].lower()
        return domain not in PUBLIC_EMAIL_DOMAINS
    except Exception:
        return False


def is_valid_phone(phone_number: str) -> bool:
    """
    Validate international phone number.
    Example:
        +919876543210
        +14155552671
    """
    try:
        parsed = phonenumbers.parse(phone_number, None)

        return (
            phonenumbers.is_valid_number(parsed)
            and phonenumbers.is_possible_number(parsed)
        )

    except Exception:
        return False


def validate_password(password: str):
    """
    Validate password strength.
    This will be used in Step 2 (Create Password).
    """

    if len(password) < 8:
        return (
            False,
            "Password must be at least 8 characters long."
        )

    if not any(c.isupper() for c in password):
        return (
            False,
            "Password must contain at least one uppercase letter."
        )

    if not any(c.islower() for c in password):
        return (
            False,
            "Password must contain at least one lowercase letter."
        )

    if not any(c.isdigit() for c in password):
        return (
            False,
            "Password must contain at least one number."
        )

    if not any(c in "!@#$%^&*()_+-=[]{}|;:',.<>?/`~" for c in password):
        return (
            False,
            "Password must contain at least one special character."
        )

    return (
        True,
        None
    )