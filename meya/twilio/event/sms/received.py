from dataclasses import dataclass
from meya.twilio.event.sms.base import TwilioSmsStatusBaseEvent


@dataclass
class TwilioSmsStatusReceivedEvent(TwilioSmsStatusBaseEvent):
    pass
