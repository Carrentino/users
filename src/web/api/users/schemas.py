from pydantic import BaseModel, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber


class UserRegistrationReq(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: PhoneNumber
    password: str
