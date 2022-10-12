from dataclasses import dataclass
from meya.front.payload import FrontPayload
from meya.http.payload.field import payload_field


@dataclass
class FrontTagTargetData(FrontPayload):
    id: str = payload_field()
    name: str = payload_field()


@dataclass
class FrontTagTarget(FrontPayload):
    data: FrontTagTargetData = payload_field()
