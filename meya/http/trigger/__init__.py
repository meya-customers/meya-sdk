from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.element.field import process_field
from meya.http.event.webhook import WebhookEvent
from meya.trigger.element import Trigger
from typing import Any


@dataclass
class WebhookTrigger(Trigger):
    is_abstract: bool = meta_field(value=True)

    when: Any = element_field(default=True)

    entry: WebhookEvent = process_field()
    encrypted_entry: WebhookEvent = process_field()
