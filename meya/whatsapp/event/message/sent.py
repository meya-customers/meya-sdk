from dataclasses import dataclass
from meya.twilio.event.sms.sent import TwilioSmsStatusSentEvent


@dataclass
class WhatsAppSentEvent(TwilioSmsStatusSentEvent):
    pass
