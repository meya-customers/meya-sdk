from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.google.actions.event import GoogleActionsEvent


@dataclass
class GoogleActionsIntentEvent(GoogleActionsEvent):
    name: str = entry_field()
