from dataclasses import dataclass
from meya.http.payload.field import payload_field
from meya.twilio.payload.payload import TwilioPayload
from typing import Optional


@dataclass
class CreateFlexChannelResponse(TwilioPayload):
    date_created: Optional[str] = payload_field(default=None)
    date_updated: Optional[str] = payload_field(default=None)
    flex_flow_sid: Optional[str] = payload_field(default=None)
    user_sid: Optional[str] = payload_field(default=None)
    task_sid: Optional[str] = payload_field(default=None)
    url: Optional[str] = payload_field(default=None)
    account_sid: Optional[str] = payload_field(default=None)
    sid: Optional[str] = payload_field(default=None)
    code: Optional[int] = payload_field(default=None)
    message: Optional[str] = payload_field(default=None)
    more_info: Optional[str] = payload_field(default=None)
    status: Optional[int] = payload_field(default=None)
