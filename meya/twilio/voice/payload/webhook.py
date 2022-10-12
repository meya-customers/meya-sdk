from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from meya.util.dict import NONE_FACTORY
from meya.util.enum import SimpleEnum
from typing import Optional


class TwilioVoiceWebhookStatus(SimpleEnum):
    QUEUED = "queued"
    RINGING = "ringing"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"
    BUSY = "busy"
    FAILED = "failed"
    NO_ANSWER = "no-answer"
    CANCELED = "canceled"


class TwilioVoiceWebhookDirection(SimpleEnum):
    INBOUND = "inbound"
    OUTBOUND_API = "outbound-api"


@dataclass
class TwilioVoiceWebhookPayload(Payload):
    To: str = payload_field()
    From: str = payload_field()
    Called: str = payload_field()
    Caller: str = payload_field()
    Digits: Optional[str] = payload_field(default_factory=NONE_FACTORY)
    StableSpeechResult: Optional[str] = payload_field(
        default_factory=NONE_FACTORY
    )
    SpeechResult: Optional[str] = payload_field(default_factory=NONE_FACTORY)
    Confidence: Optional[float] = payload_field(default_factory=NONE_FACTORY)
    CallSid: str = payload_field()
    ToState: str = payload_field()
    Direction: TwilioVoiceWebhookDirection = payload_field()
    ToCountry: str = payload_field()
    AccountSid: str = payload_field()
    ApiVersion: str = payload_field()
    CallStatus: TwilioVoiceWebhookStatus = payload_field()
    CalledState: str = payload_field()
    FromCountry: str = payload_field()
    CalledCountry: str = payload_field()
    CallerCountry: str = payload_field()

    @property
    def user_id(self) -> str:
        return (
            self.To
            if self.Direction == TwilioVoiceWebhookDirection.OUTBOUND_API
            else self.From
        )
