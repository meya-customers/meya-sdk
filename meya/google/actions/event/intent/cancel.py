from dataclasses import dataclass
from meya.google.actions.event.intent import GoogleActionsIntentEvent


@dataclass
class GoogleActionsCancelEvent(GoogleActionsIntentEvent):
    pass
