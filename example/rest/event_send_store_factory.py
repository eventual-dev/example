from typing import AsyncGenerator

import anyio
from eventual.event_store import EventSendStore
from eventual_tortoise.event_store import TortoiseEventSendStore

event_body_send_stream, event_body_stream = anyio.create_memory_object_stream()


async def create_event_send_store() -> AsyncGenerator[EventSendStore, None]:
    async with anyio.create_task_group() as task_group:
        yield TortoiseEventSendStore(event_body_send_stream.clone(), task_group)
