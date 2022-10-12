from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from typing import ClassVar
from typing import List
from typing import Optional


@dataclass
class TeckstBasePayload(Payload):
    to_camel_case_fields: ClassVar[bool] = True
    crm_channel_identifier: str = payload_field()
    contact_channel_identifier: str = payload_field()


@dataclass
class TeckstMedia(Payload):
    url: str = payload_field()


@dataclass
class TeckstSendMessagePayload(TeckstBasePayload):
    crm: str = payload_field()
    status: str = payload_field(default="open")
    body: Optional[str] = payload_field(default=None)
    media: Optional[List[TeckstMedia]] = payload_field(default=None)


@dataclass
class TeckstMediaWebhook(TeckstMedia):
    long_url: str = payload_field()


@dataclass
class TeckstWebhook(TeckstBasePayload):
    media: List[TeckstMediaWebhook] = payload_field(default_factory=list)
    content: Optional[str] = payload_field(default=None)
