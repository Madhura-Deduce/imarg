from pydantic import BaseModel
from typing import Optional


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    subscription_type: str


class UserProfileResponse(BaseModel):
    success: bool
    user: UserResponse