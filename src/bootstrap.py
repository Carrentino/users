from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Any

from aiokafka import AIOKafkaConsumer
from aiokafka.util import create_task
from fastapi import APIRouter, FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import UJSONResponse
from helpers.api.bootstrap.setup_error_handlers import setup_error_handlers
from helpers.api.middleware.auth import AuthMiddleware
from helpers.api.middleware.trace_id.middleware import TraceIdMiddleware
from helpers.api.middleware.unexpected_errors.middleware import ErrorsHandlerMiddleware
from helpers.sqlalchemy.client import SQLAlchemyClient
from prometheus_fastapi_instrumentator import Instrumentator
from pydantic import PostgresDsn

from src.kafka.payment.views import payment_listener
from src.kafka.user.views import user_listener
from src.settings import get_settings
from src.web.api.me.views import me_router
from src.web.api.users.views import users_router


@lru_cache
def make_db_client(dsn: PostgresDsn = get_settings().postgres_dsn) -> SQLAlchemyClient:
    return SQLAlchemyClient(dsn=dsn)


@asynccontextmanager
async def _lifespan(
    app: FastAPI,  # noqa
) -> AsyncGenerator[dict[str, Any], None]:
    client = make_db_client()
    kafka_consumer = AIOKafkaConsumer(
        *get_settings().kafka.topics,
        bootstrap_servers=get_settings().kafka.bootstrap_servers,
        group_id=get_settings().kafka.group_id,
    )
    await kafka_consumer.start()
    create_task(payment_listener.listen(kafka_consumer))
    create_task(user_listener.listen(kafka_consumer))
    try:
        yield {
            'db_client': client,
        }
    finally:
        await client.close()
        await kafka_consumer.stop()


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(ErrorsHandlerMiddleware, is_debug=get_settings().debug)  # type: ignore
    app.add_middleware(TraceIdMiddleware)  # type: ignore
    app.add_middleware(AuthMiddleware, key=get_settings().jwt_key)  # type: ignore


def setup_api_routers(app: FastAPI) -> None:
    api_router = APIRouter(prefix='/users/api')
    api_router.include_router(users_router, prefix='/users', tags=['users'])
    api_router.include_router(me_router, prefix='/me', tags=['me'])
    app.include_router(router=api_router)


def setup_prometheus(app: FastAPI) -> None:
    Instrumentator(should_group_status_codes=False).instrument(app).expose(
        app, should_gzip=True, name='prometheus_metrics', endpoint='/metrics'
    )


def make_app() -> FastAPI:
    app = FastAPI(
        title='users',
        lifespan=_lifespan,
        docs_url='/users/api/docs',
        redoc_url='/users/api/redoc',
        openapi_url='/users/api/openapi.json',
        default_response_class=UJSONResponse,
    )

    setup_error_handlers(app, is_debug=get_settings().debug)
    setup_prometheus(app)
    setup_api_routers(app)
    setup_middlewares(app)

    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=app.title,
            version="1.0.0",
            description="API documentation for orders service",
            routes=app.routes,
        )
        openapi_schema["components"]["securitySchemes"] = {
            "X-Auth-Token": {
                "type": "apiKey",
                "in": "header",
                "name": "X-Auth-Token",
            }
        }
        for path in openapi_schema["paths"].values():
            for method in path.values():
                method["security"] = [{"X-Auth-Token": []}]
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    app.openapi = custom_openapi

    return app
