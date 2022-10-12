from dataclasses import dataclass
from enum import Enum
from meya.http.payload.field import payload_field
from meya.twilio.payload import TwilioPayload
from typing import Optional
from typing import Tuple


class TwilioMessageStatus(Enum):
    ACCEPTED = "accepted"
    QUEUED = "queued"
    SENDING = "sending"
    SENT = "sent"
    FAILED = "failed"
    DELIVERED = "delivered"
    UNDELIVERED = "undelivered"
    RECEIVING = "receiving"
    RECEIVED = "received"
    READ = "read"


@dataclass
class TwilioWebhook(TwilioPayload):
    """
    https://www.twilio.com/docs/sms/twiml#twilios-request-to-your-application
    """

    ApiVersion: str = payload_field()
    MessageSid: str = payload_field()
    AccountSid: str = payload_field()
    From: str = payload_field()
    To: str = payload_field()

    Body: Optional[str] = payload_field(default=None)
    WaId: Optional[str] = payload_field(default=None)

    ProfileName: Optional[str] = payload_field(default=None)

    SmsStatus: Optional[TwilioMessageStatus] = payload_field(default=None)
    SmsSid: Optional[str] = payload_field(default=None)

    ToCity: Optional[str] = payload_field(default=None)

    ToState: Optional[str] = payload_field(default=None)
    FromState: Optional[str] = payload_field(default=None)

    ToCountry: Optional[str] = payload_field(default=None)
    FromCountry: Optional[str] = payload_field(default=None)

    NumSegments: Optional[str] = payload_field(default=None)
    SmsMessageSid: Optional[str] = payload_field(default=None)

    MessagingServiceSid: Optional[str] = payload_field(default=None)
    NumMedia: Optional[str] = payload_field(default=None)

    ChannelPrefix: Optional[str] = payload_field(default=None)
    MessageStatus: Optional[str] = payload_field(default=None)
    ChannelToAddress: Optional[str] = payload_field(default=None)
    ChannelInstallSid: Optional[str] = payload_field(default=None)

    StructuredMessage: Optional[str] = payload_field(default=None)

    # media (up to 10 media items)
    MediaContentType0: Optional[str] = payload_field(default=None)
    MediaUrl0: Optional[str] = payload_field(default=None)
    MediaContentType1: Optional[str] = payload_field(default=None)
    MediaUrl1: Optional[str] = payload_field(default=None)
    MediaContentType2: Optional[str] = payload_field(default=None)
    MediaUrl2: Optional[str] = payload_field(default=None)
    MediaContentType3: Optional[str] = payload_field(default=None)
    MediaUrl3: Optional[str] = payload_field(default=None)
    MediaContentType4: Optional[str] = payload_field(default=None)
    MediaUrl4: Optional[str] = payload_field(default=None)
    MediaContentType5: Optional[str] = payload_field(default=None)
    MediaUrl5: Optional[str] = payload_field(default=None)
    MediaContentType6: Optional[str] = payload_field(default=None)
    MediaUrl6: Optional[str] = payload_field(default=None)
    MediaContentType7: Optional[str] = payload_field(default=None)
    MediaUrl7: Optional[str] = payload_field(default=None)
    MediaContentType8: Optional[str] = payload_field(default=None)
    MediaUrl8: Optional[str] = payload_field(default=None)
    MediaContentType9: Optional[str] = payload_field(default=None)
    MediaUrl9: Optional[str] = payload_field(default=None)
    MediaContentType10: Optional[str] = payload_field(default=None)
    MediaUrl10: Optional[str] = payload_field(default=None)

    @property
    def is_message(self) -> bool:
        return bool(self.Body) or bool(self.MediaUrl0)

    @property
    def is_structured(self) -> bool:
        return self.StructuredMessage == "true"

    @property
    def num_media(self) -> int:
        try:
            return int(self.NumMedia)
        except (ValueError, TypeError):
            return 0

    @property
    def to_phone_number(self) -> str:
        return self._split_phone_number(self.To)[0]

    @property
    def to_channel(self) -> str:
        return self._split_phone_number(self.To)[1]

    @property
    def from_phone_number(self) -> str:
        return self._split_phone_number(self.From)[0]

    @property
    def from_channel(self) -> str:
        return self._split_phone_number(self.From)[1]

    @staticmethod
    def _split_phone_number(phone_number: str) -> Tuple[str, str]:
        parts = phone_number.split(":")
        if len(parts) > 1:
            channel = parts[0]
            phone_number = parts[1]
        else:
            channel = "sms"
            phone_number = parts[0]
        return phone_number, channel
