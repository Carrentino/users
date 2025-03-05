from helpers.errors import BaseError
from pydantic import BaseModel


class UserAlreadyExistsError(BaseError):
    message = 'User with this email already exists'


class UserNotFoundError(BaseError):
    message = 'User not found'


class InvalidUserStatusError(BaseError):
    message = 'User has invalid status'


class InvalidCodeError(BaseError):
    message = 'Invalid code'


class WrongPasswordError(BaseModel):
    message = 'Wrong password'
