from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.orb.event.device import DeviceEvent


@dataclass
class HeartbeatEvent(DeviceEvent):
    timestamp: int = entry_field()
