from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.orb.event.device import DeviceEvent
from meya.orb.event.device.state import DeviceState
from meya.util.enum import SimpleEnum


class Platform(SimpleEnum):
    ANDROID = "android"
    IOS = "ios"
    WEB = "web"


@dataclass
class ConnectEvent(DeviceEvent):
    device_token: str = entry_field(sensitive=True)
    state: DeviceState = entry_field()
    platform: Platform = entry_field()
