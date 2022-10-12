from dataclasses import dataclass
from meya.calendly.event import CalendlyEvent


@dataclass
class CalendlyInviteeCreatedEvent(CalendlyEvent):
    pass
