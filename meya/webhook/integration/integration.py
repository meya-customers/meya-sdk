from dataclasses import dataclass
from meya.element.field import element_field
from meya.integration.element.interactive import InteractiveIntegration
from typing import ClassVar


@dataclass
class WebhookIntegration(InteractiveIntegration):
    NAME: ClassVar[str] = "webhook"

    api_key: str = element_field()
    postback_url: str = element_field()
    suppress_echo: bool = element_field(default=True)
    decrypt_tx: bool = element_field(default=False)
    redact_tx: bool = element_field(default=False)
