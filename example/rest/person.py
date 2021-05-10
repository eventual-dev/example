from eventual.event_store import EventSendStore
from fastapi import APIRouter, Depends

from example.app.payment_case import pay
from example.rest import event_send_store_factory

router = APIRouter(
    prefix="/person",
    tags=["person"],
)


@router.post("/pay")
async def create_unit(
    event_send_store: EventSendStore = Depends(
        event_send_store_factory.create_event_send_store
    ),
) -> None:
    await pay(event_send_store)
