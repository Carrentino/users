from helpers.errors import ServerError
from starlette import status


class UserAlreadyExistsErrorHttpError(ServerError):
    status_code = status.HTTP_400_BAD_REQUEST
    message = 'User with this email already exists'
