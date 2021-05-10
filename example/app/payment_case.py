import asyncio

from eventual.broker import Message
from eventual.event_store import EventSendStore, Guarantee

from example.model.person import Person
from example.registry import eventual_registry


async def pay(event_send_store: EventSendStore) -> None:
    p = Person.from_name("Jack")
    async with event_send_store.clear_outbox_in_work_unit(p):
        p.pay()


@eventual_registry.subscribe(["payment-requested"], guarantee=Guarantee.EXACTLY_ONCE)
async def payment_requested_handler(message: Message, _: EventSendStore) -> None:
    await asyncio.sleep(5)

    print("important_handler", message)


@eventual_registry.subscribe(["payment-approved"], guarantee=Guarantee.AT_LEAST_ONCE)
async def payment_approved_handler(message: Message, _: EventSendStore) -> None:
    await asyncio.sleep(1)
    print("abc_handler", message)


@eventual_registry.subscribe(
    ["payment-succeeded"], guarantee=Guarantee.NO_MORE_THAN_ONCE
)
async def payment_dispatched_handler(message: Message, _: EventSendStore) -> None:
    print("xyz handler", message)
