from helpers.errors import ServerError
from starlette import status


class UserAlreadyExistsErrorHttpError(ServerError):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'User with this email already exists'


class UserNotFoundHttpError(ServerError):
    status_code = status.HTTP_404_NOT_FOUND
    message = 'User not found'


class InvalidUserStatusHttpError(ServerError):
    status_code = status.HTTP_403_FORBIDDEN
    message = 'User has invalid status'


class InvalidCodeHttpError(ServerError):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'Invalid code'


class WrongPasswordHttpError(ServerError):
    status_code = status.HTTP_403_FORBIDDEN
    message = 'Wrong password'
