from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.front.payload.message import FrontPartnerChannelMessage
from meya.front.payload.message import FrontPartnerChannelMetadata
from meya.http.event.webhook import WebhookEvent


@dataclass
class FrontUnhandledEvent(WebhookEvent):
    payload: FrontPartnerChannelMessage = entry_field(sensitive=True)
    metadata: FrontPartnerChannelMetadata = entry_field()
