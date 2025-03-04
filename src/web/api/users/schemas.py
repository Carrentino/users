from uuid import UUID

from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserRegistrationReq(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: PhoneNumber
    password: str


class VerifyTokenReq(BaseModel):
    user_id: UUID
    code: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
