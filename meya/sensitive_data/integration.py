from dataclasses import dataclass
from dataclasses import field
from datetime import timedelta
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.integration.element import Integration
from meya.sensitive_data.config import SENSITIVE_DATA_TTL
from meya.sensitive_data.config import SENSITIVE_EVENT_TTL
from meya.time.timedelta import from_timedelta
from typing import ClassVar
from typing import Type


@dataclass
class LedgerSensitiveDataConfigSpec:
    sensitive_ttl: timedelta = field(default=SENSITIVE_DATA_TTL)

    def validate(self, element: Element, name):
        if self.sensitive_ttl > SENSITIVE_DATA_TTL:
            raise element.validation_error(
                f"{name} cannot have a sensitive_ttl longer than "
                f"{from_timedelta(SENSITIVE_DATA_TTL)}"
            )


@dataclass
class EventSensitiveDataConfigSpec:
    sensitive_ttl: timedelta = field(default=SENSITIVE_EVENT_TTL)

    def validate(self, element: Element, name):
        if self.sensitive_ttl > SENSITIVE_EVENT_TTL:
            raise element.validation_error(
                f"{name} cannot have a sensitive_ttl longer than "
                f"{from_timedelta(SENSITIVE_EVENT_TTL)}"
            )


@dataclass
class SensitiveDataIntegration(Integration):
    NAME: ClassVar[str] = "sensitive_data"
    DEFAULT_ID: ClassVar[str] = "integration.sensitive_data"

    transport: bool = element_field(
        default=True, help="Enables sensitive HTTP and WS entries"
    )
    transcript: bool = element_field(
        default=True, help="Enables sensitive events and flow-scope data"
    )
    bot_ledger: LedgerSensitiveDataConfigSpec = element_field(
        default_factory=LedgerSensitiveDataConfigSpec
    )
    event_ledger: EventSensitiveDataConfigSpec = element_field(
        default_factory=EventSensitiveDataConfigSpec
    )
    http_ledger: LedgerSensitiveDataConfigSpec = element_field(
        default_factory=LedgerSensitiveDataConfigSpec
    )
    log_ledger: LedgerSensitiveDataConfigSpec = element_field(
        default_factory=LedgerSensitiveDataConfigSpec
    )
    presence_ledger: LedgerSensitiveDataConfigSpec = element_field(
        default_factory=LedgerSensitiveDataConfigSpec
    )
    thread_ledger: LedgerSensitiveDataConfigSpec = element_field(
        default_factory=LedgerSensitiveDataConfigSpec
    )
    user_ledger: LedgerSensitiveDataConfigSpec = element_field(
        default_factory=LedgerSensitiveDataConfigSpec
    )
    ws_ledger: LedgerSensitiveDataConfigSpec = element_field(
        default_factory=LedgerSensitiveDataConfigSpec
    )
    blob: EventSensitiveDataConfigSpec = element_field(
        default_factory=EventSensitiveDataConfigSpec
    )

    def validate(self):
        super().validate()
        if self.id != self.DEFAULT_ID:
            raise self.validation_error(
                f"{self.DEFAULT_ID} is the only supported ID for this integration"
            )
        self.bot_ledger.validate(self, "bot_ledger")
        self.event_ledger.validate(self, "event_ledger")
        self.http_ledger.validate(self, "http_ledger")
        self.log_ledger.validate(self, "log_ledger")
        self.presence_ledger.validate(self, "presence_ledger")
        self.thread_ledger.validate(self, "thread_ledger")
        self.user_ledger.validate(self, "user_ledger")
        self.ws_ledger.validate(self, "ws_ledger")
        self.blob.validate(self, "blob")

    async def accept(self) -> bool:
        return False

    @classmethod
    def create_default(cls) -> "SensitiveDataIntegration":
        return cls(id=cls.DEFAULT_ID, enabled=False)


class SensitiveDataIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = SensitiveDataIntegration

    @classmethod
    def create_default(cls) -> "SensitiveDataIntegrationRef":
        return SensitiveDataIntegrationRef(SensitiveDataIntegration.DEFAULT_ID)
