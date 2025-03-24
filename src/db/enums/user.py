from enum import StrEnum


class UserStatus(StrEnum):
    NOT_VERIFIED = 'Не верифицирован'
    VERIFIED = 'Верифицирован'
    SUSPECTED = 'Подозреваемый'
    BANNED = 'Заблокирован'
