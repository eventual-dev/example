import dataclasses
import uuid
from typing import Type, TypeVar

from eventual.model import Entity, Event

P = TypeVar("P", bound="Person")


@dataclasses.dataclass(frozen=True)
class PaymentRequested(Event):
    pass


@dataclasses.dataclass(frozen=True)
class PaymentApproved(Event):
    pass


@dataclasses.dataclass(frozen=True)
class PaymentSucceeded(Event):
    pass


class Person(Entity[uuid.UUID]):
    def __init__(self, *, unique_id: uuid.UUID, name: str):
        super().__init__(unique_id=unique_id)
        self.name = name

    @classmethod
    def from_name(cls: Type[P], name: str) -> P:
        return cls._create(unique_id=uuid.uuid4(), name=name)

    def pay(self) -> None:
        self._outbox.append(PaymentRequested())
        self._outbox.append(PaymentApproved())
        self._outbox.append(PaymentSucceeded())
