from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.presence.event import PresenceEvent
from typing import Any


@dataclass
class DeviceEvent(PresenceEvent):
    device_id: str = entry_field()
    key: str = entry_field()
    value: Any = entry_field()
