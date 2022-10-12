from dataclasses import dataclass
from datetime import date
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from meya.twilio.voice.payload.webhook import TwilioVoiceWebhookDirection
from typing import Optional


@dataclass
class TwilioVoiceCallPayload(Payload):
    to: str = payload_field()
    sid: str = payload_field()
    uri: str = payload_field()
    from_: str = payload_field(key="from")
    status: str = payload_field()
    direction: TwilioVoiceWebhookDirection = payload_field()
    price_unit: str = payload_field()
    queue_time: str = payload_field()
    account_sid: str = payload_field()
    api_version: str = payload_field()
    to_formatted: str = payload_field()
    from_formatted: str = payload_field()
    phone_number_sid: str = payload_field()
    subresource_uris: dict = payload_field()
    start_time: Optional[str] = payload_field(default=None)
    parent_call_sid: Optional[str] = payload_field(default=None)
    forwarded_from: Optional[str] = payload_field(default=None)
    caller_name: Optional[str] = payload_field(default=None)
    date_created: Optional[date] = payload_field(default=None)
    date_updated: Optional[date] = payload_field(default=None)
    answered_by: Optional[str] = payload_field(default=None)
    group_sid: Optional[str] = payload_field(default=None)
    trunk_sid: Optional[str] = payload_field(default=None)
    annotation: Optional[str] = payload_field(default=None)
    duration: Optional[str] = payload_field(default=None)
    end_time: Optional[str] = payload_field(default=None)
    price: Optional[str] = payload_field(default=None)
