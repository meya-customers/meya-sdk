from dataclasses import dataclass
from meya.http.payload.field import payload_field
from meya.zendesk.support.payload import ZendeskSupportPayload


@dataclass
class ZendeskSupportAttachment(ZendeskSupportPayload):
    id: int = payload_field()
    file_name: str = payload_field()
    content_url: str = payload_field()
    content_type: str = payload_field()
