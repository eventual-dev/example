from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
import uvicorn

from eventual.dispatch.concurrent_dispatcher import ConcurrentMessageDispatcher
from eventual.util.asgi import eventual_concurrent_lifespan

from eventual_rmq.broker import RmqMessageBroker
from eventual_tortoise.event_store import (
    TortoiseEventSendStore,
    TortoiseEventReceiveStore,
)

from example import configuration
from example.ls import tortoise_lifespan
from example.registry import eventual_registry
from example.rest import person
from example.rest import event_send_store_factory


def build_router() -> APIRouter:
    router = APIRouter()
    router.include_router(person.router)
    return router


def get_app():
    app = FastAPI(debug=configuration.DEBUG, title="Example")

    message_broker = RmqMessageBroker(
        configuration.AMQP_DSN,
        configuration.AMQP_EXCHANGE,
        configuration.AMQP_QUEUE,
    )
    event_receive_store = TortoiseEventReceiveStore()

    async def lifespan_context(a):
        tortoise_context = asynccontextmanager(
            tortoise_lifespan(
                config=dict(
                    apps=dict(payment=dict(models=["eventual_tortoise.relation"])),
                    connections=dict(default=configuration.DB_DSN),
                    use_tz=False,
                    timezone="UTC",
                ),
                # generate_schemas=True,
            )
        )
        eventual_context = asynccontextmanager(
            eventual_concurrent_lifespan(
                eventual_registry,
                message_broker,
                event_receive_store,
                (
                    event_send_store_factory.event_body_send_stream,
                    event_send_store_factory.event_body_stream,
                ),
                TortoiseEventSendStore,
                ConcurrentMessageDispatcher,
            )
        )
        async with tortoise_context(a):
            async with eventual_context(a):
                yield

    app.router.lifespan_context = lifespan_context
    app.include_router(build_router())
    return app


APP = get_app()

if __name__ == "__main__":
    uvicorn.run(APP, host="0.0.0.0", port=8000, lifespan="on")
