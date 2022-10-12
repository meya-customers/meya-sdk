from dataclasses import dataclass
from meya.event.entry.interactive import InteractiveEvent


@dataclass
class WidgetEvent(InteractiveEvent):
    pass
