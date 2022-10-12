from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.event.entry import Event


@dataclass
class TwilioFlexReservationCompletedEvent(Event):
    task_attributes: dict = entry_field()
    worker_attributes: dict = entry_field()
