from dataclasses import dataclass
from dataclasses import field
from datetime import timedelta
from meya.db.config import LEDGER_MAXLEN
from meya.db.config import LEDGER_VIEW_TTL
from meya.db.config import QUEUE_MAXLEN
from meya.db.config import REQUEST_RESPONSE_LEDGER_MAXLEN
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.integration.element import Integration
from meya.time.timedelta import from_timedelta
from typing import ClassVar
from typing import Type


@dataclass
class DbQueueConfigSpec:
    cache_maxlen: int = field(default=QUEUE_MAXLEN)

    def validate(self, element: Element, name):
        if self.cache_maxlen > QUEUE_MAXLEN:
            raise element.validation_error(
                f"{name} cannot have a cache_maxlen greater than "
                f"{QUEUE_MAXLEN}"
            )


@dataclass
class DbLedgerConfigSpec:
    cache_maxlen: int = field(default=LEDGER_MAXLEN)
    cache_ttl: timedelta = field(default=LEDGER_VIEW_TTL)
    persist: bool = field(default=True)

    def validate(self, element: Element, name):
        if self.cache_maxlen > LEDGER_MAXLEN:
            raise element.validation_error(
                f"{name} cannot have a cache_maxlen greater than "
                f"{LEDGER_MAXLEN}"
            )
        if self.cache_ttl > LEDGER_VIEW_TTL:
            raise element.validation_error(
                f"{name} cannot have a cache_ttl longer than "
                f"{from_timedelta(LEDGER_VIEW_TTL)}"
            )


@dataclass
class DbHashViewConfigSpec:
    cache_ttl: timedelta = field(default=LEDGER_VIEW_TTL)
    persist: bool = field(default=True)

    def validate(self, element: Element, name):
        if self.cache_ttl > LEDGER_VIEW_TTL:
            raise element.validation_error(
                f"{name} cannot have a cache_ttl longer than "
                f"{from_timedelta(LEDGER_VIEW_TTL)}"
            )


@dataclass
class PresenceLedgerConfigSpec(DbLedgerConfigSpec):
    persist: bool = field(default=False)


@dataclass
class PresenceHashViewConfigSpec(DbHashViewConfigSpec):
    persist: bool = field(default=False)


@dataclass
class WsLedgerConfigSpec(DbLedgerConfigSpec):
    cache_maxlen: int = field(default=REQUEST_RESPONSE_LEDGER_MAXLEN)
    persist: bool = field(default=False)

    def validate(self, element: Element, name):
        if self.cache_maxlen > REQUEST_RESPONSE_LEDGER_MAXLEN:
            raise element.validation_error(
                f"{name} cannot have a cache_maxlen greater than "
                f"{REQUEST_RESPONSE_LEDGER_MAXLEN}"
            )
        super().validate(element, name)


@dataclass
class DbIntegration(Integration):
    NAME: ClassVar[str] = "db"
    DEFAULT_ID: ClassVar[str] = "integration.db"

    presence_queue: DbQueueConfigSpec = element_field(
        default_factory=DbQueueConfigSpec
    )
    presence_ledger: PresenceLedgerConfigSpec = element_field(
        default_factory=PresenceLedgerConfigSpec
    )
    presence_device_view: PresenceHashViewConfigSpec = element_field(
        default_factory=PresenceHashViewConfigSpec
    )
    ws_queue: DbQueueConfigSpec = element_field(
        default_factory=DbQueueConfigSpec
    )
    ws_ledger: WsLedgerConfigSpec = element_field(
        default_factory=WsLedgerConfigSpec
    )

    def validate(self):
        super().validate()
        if self.id != self.DEFAULT_ID:
            raise self.validation_error(
                f"{self.DEFAULT_ID} is the only supported ID for this "
                f"integration"
            )
        self.presence_queue.validate(self, "presence_queue")
        self.presence_ledger.validate(self, "presence_ledger")
        self.presence_device_view.validate(self, "presence_device_view")
        self.ws_queue.validate(self, "ws_queue")
        self.ws_ledger.validate(self, "ws_ledger")

    async def accept(self) -> bool:
        return False

    @classmethod
    def create_default(cls) -> "DbIntegration":
        return cls(id=cls.DEFAULT_ID, enabled=False)


class DbIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = DbIntegration

    @classmethod
    def create_default(cls) -> "DbIntegrationRef":
        return DbIntegrationRef(DbIntegration.DEFAULT_ID)
