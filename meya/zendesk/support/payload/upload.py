from dataclasses import dataclass
from meya.http.payload.field import payload_field
from meya.zendesk.support.payload import ZendeskSupportPayload
from meya.zendesk.support.payload.attachment import ZendeskSupportAttachment
from typing import List


@dataclass
class ZendeskUpload(ZendeskSupportPayload):
    token: str = payload_field()
    attachment: ZendeskSupportAttachment = payload_field()
    attachments: List[ZendeskSupportAttachment] = payload_field()


@dataclass
class ZendeskUploadResponse(ZendeskSupportPayload):
    upload: ZendeskUpload = payload_field()
