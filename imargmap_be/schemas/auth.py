from pydantic import BaseModel, EmailStr, field_validator
import phonenumbers


class RegisterRequest(BaseModel):
    full_name: str
    email: EmailStr
    country: str      # Example: "IN", "LB", "US"
    phone_number: str
    company_name: str
    location: str

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value, info):

        country = info.data.get("country")

        try:
            parsed = phonenumbers.parse(value, country)

            if not phonenumbers.is_valid_number(parsed):
                raise ValueError

        except Exception:
            raise ValueError(
                f"Please enter a valid phone number for {country}."
            )

        return phonenumbers.format_number(
            parsed,
            phonenumbers.PhoneNumberFormat.E164
        )


class CreateAccountRequest(BaseModel):
    token: str
    password: str
    confirm_password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):

        if len(value) < 8:
            raise ValueError(
                "Password must be at least 8 characters long."
            )

        if not any(c.isupper() for c in value):
            raise ValueError(
                "Password must contain at least one uppercase letter."
            )

        if not any(c.islower() for c in value):
            raise ValueError(
                "Password must contain at least one lowercase letter."
            )

        if not any(c.isdigit() for c in value):
            raise ValueError(
                "Password must contain at least one number."
            )

        if not any(
            c in "!@#$%^&*()_+-=[]{}|;:',.<>?/`~"
            for c in value
        ):
            raise ValueError(
                "Password must contain at least one special character."
            )

        return value

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, value, info):

        password = info.data.get("password")

        if password != value:
            raise ValueError(
                "Passwords do not match."
            )

        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class VerifyEmailRequest(BaseModel):
    token: str


class ApiKeyResponse(BaseModel):
    api_key: str