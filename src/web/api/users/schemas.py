from uuid import UUID

from fastapi.params import Query
from pydantic import BaseModel, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserRegistrationReq(BaseModel):
    email: EmailStr


class VerifyTokenReq(BaseModel):
    code: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: PhoneNumber
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserLoginReq(BaseModel):
    email: EmailStr
    password: str


class UsersFilterId(BaseModel):
    user__id: list[UUID] = Field(Query(list))


class UserFI(BaseModel):
    id: UUID
    first_name: str
    last_name: str

    class Config:
        from_attributes = True


class ChangePasswordSendCodeReq(BaseModel):
    email: EmailStr


class ChangePasswordTokenReq(BaseModel):
    code: str
    email: EmailStr
    password: str
