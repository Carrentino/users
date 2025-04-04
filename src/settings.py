from functools import lru_cache

from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AuthSettings(BaseSettings):
    algorithm: str = Field(default='HS256')
    secret_key: SecretStr = Field(default=SecretStr('551b8ef09b5e43ddcc45461f854a89b83b9277c6e578f750bf5a6bc3f06d8c08'))
    access_lifetime: int = Field(default=7)
    refresh_lifetime: int = Field(default=15)

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
        extra='ignore',
    )


class RedisSettings(BaseSettings):
    url: str = Field(default='redis://localhost:6379')
    balance_db: int = Field(default=0)
    email_code_db: int = Field(default=1)

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
        extra='ignore',
        env_prefix='redis_',
    )


class KafkaSettings(BaseSettings):
    bootstrap_servers: str = Field(default='localhost:9092')
    group_id: str = Field(default='users-group')
    topic_user_balance: str = Field(default='users_balance')
    topic_user_score: str = Field(default='users_score')
    notifications_url: str = Field(default='')
    topic_email_notifications: str = Field(default='notifications_mails')

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
        extra='ignore',
        env_prefix='kafka_',
    )

    @property
    def topics(self) -> list[str]:
        return [v for k, v in self.__dict__.items() if k.startswith('topic_')]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
        extra='ignore',
    )

    host: str = '0.0.0.0'  # noqa: S104
    port: int = 8080
    workers_count: int = 1
    reload: bool = True

    log_level: str = Field(default='info')
    debug: bool = False
    debug_postgres: bool = False

    environment: str = 'dev'

    postgres_dsn: PostgresDsn = Field(  # type: ignore
        default='postgresql+asyncpg://postgres:postgres@localhost:5432/base'
    )
    test_postgres_dsn: PostgresDsn = Field(  # type: ignore
        default='postgresql+asyncpg://postgres:@localhost:5432/base_test'
    )

    trace_id_header: str = 'X-Trace-Id'
    jwt_key: SecretStr = Field(default=SecretStr('551b8ef09b5e43ddcc45461f854a89b83b9277c6e578f750bf5a6bc3f06d8c08'))

    redis: RedisSettings = RedisSettings()
    kafka: KafkaSettings = KafkaSettings()
    auth_settings: AuthSettings = AuthSettings()
    reviews_url: str = Field(default='http://localhost:8080/reviews')
    cars_url: str = Field(default='http://localhost:8080/cars')


@lru_cache
def get_settings() -> Settings:
    return Settings()
