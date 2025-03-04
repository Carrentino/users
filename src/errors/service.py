from helpers.errors import BaseError


class UserAlreadyExistsError(BaseError):
    message = 'User with this email already exists'
