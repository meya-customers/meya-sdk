from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.http.event.webhook import WebhookEvent
from meya.twilio.payload.webhook import TwilioMessageStatus
from typing import Optional


@dataclass
class TwilioSmsStatusBaseEvent(WebhookEvent):
    MessageSid: Optional[str] = entry_field(sensitive=True, default=None)
    From: Optional[str] = entry_field(sensitive=True, default=None)
    To: Optional[str] = entry_field(sensitive=True, default=None)

    Body: Optional[str] = entry_field(sensitive=True, default=None)
    WaId: Optional[str] = entry_field(sensitive=True, default=None)

    ProfileName: Optional[str] = entry_field(sensitive=True, default=None)

    SmsStatus: Optional[TwilioMessageStatus] = entry_field(
        sensitive=True, default=None
    )
    SmsSid: Optional[str] = entry_field(sensitive=True, default=None)

    ToCity: Optional[str] = entry_field(sensitive=True, default=None)

    ToState: Optional[str] = entry_field(sensitive=True, default=None)
    FromState: Optional[str] = entry_field(sensitive=True, default=None)

    ToCountry: Optional[str] = entry_field(sensitive=True, default=None)
    FromCountry: Optional[str] = entry_field(sensitive=True, default=None)

    NumSegments: Optional[str] = entry_field(sensitive=True, default=None)
    SmsMessageSid: Optional[str] = entry_field(sensitive=True, default=None)

    MessagingServiceSid: Optional[str] = entry_field(
        sensitive=True, default=None
    )
    NumMedia: Optional[str] = entry_field(sensitive=True, default=None)

    ChannelPrefix: Optional[str] = entry_field(sensitive=True, default=None)
    MessageStatus: Optional[str] = entry_field(sensitive=True, default=None)
    ChannelToAddress: Optional[str] = entry_field(sensitive=True, default=None)
    ChannelInstallSid: Optional[str] = entry_field(
        sensitive=True, default=None
    )

    StructuredMessage: Optional[str] = entry_field(
        sensitive=True, default=None
    )

    MediaContentType0: Optional[str] = entry_field(
        sensitive=True, default=None
    )
    MediaUrl0: Optional[str] = entry_field(sensitive=True, default=None)
    MediaContentType1: Optional[str] = entry_field(
        sensitive=True, default=None
    )
    MediaUrl1: Optional[str] = entry_field(sensitive=True, default=None)
    MediaContentType2: Optional[str] = entry_field(
        sensitive=True, default=None
    )
    MediaUrl2: Optional[str] = entry_field(sensitive=True, default=None)
    MediaContentType3: Optional[str] = entry_field(
        sensitive=True, default=None
    )
    MediaUrl3: Optional[str] = entry_field(sensitive=True, default=None)
    MediaContentType4: Optional[str] = entry_field(
        sensitive=True, default=None
    )
    MediaUrl4: Optional[str] = entry_field(sensitive=True, default=None)
    MediaContentType5: Optional[str] = entry_field(
        sensitive=True, default=None
    )
    MediaUrl5: Optional[str] = entry_field(sensitive=True, default=None)
    MediaContentType6: Optional[str] = entry_field(
        sensitive=True, default=None
    )
    MediaUrl6: Optional[str] = entry_field(sensitive=True, default=None)
    MediaContentType7: Optional[str] = entry_field(
        sensitive=True, default=None
    )
    MediaUrl7: Optional[str] = entry_field(sensitive=True, default=None)
    MediaContentType8: Optional[str] = entry_field(
        sensitive=True, default=None
    )
    MediaUrl8: Optional[str] = entry_field(sensitive=True, default=None)
    MediaContentType9: Optional[str] = entry_field(
        sensitive=True, default=None
    )
    MediaUrl9: Optional[str] = entry_field(sensitive=True, default=None)
    MediaContentType10: Optional[str] = entry_field(
        sensitive=True, default=None
    )
    MediaUrl10: Optional[str] = entry_field(sensitive=True, default=None)
