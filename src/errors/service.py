from helpers.errors import BaseError


class UserAlreadyExistsError(BaseError):
    message = 'User with this email already exists'


class UserNotFoundError(BaseError):
    message = 'User not found'


class InvalidUserStatusError(BaseError):
    message = 'User has invalid status'


class InvalidCodeError(BaseError):
    message = 'Invalid code'
