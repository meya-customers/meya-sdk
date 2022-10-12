from dataclasses import dataclass
from meya.http.payload.field import payload_field
from meya.http.payload.payload import Payload
from meya.time import Timezone
from numbers import Real
from typing import List
from typing import Optional


@dataclass
class WitContextCoords(Payload):
    lat: Real = payload_field()
    long: Real = payload_field()


@dataclass
class WitContext(Payload):
    reference_time: Optional[str] = payload_field(default=None)
    timezone: Optional[Timezone] = payload_field(default=None)
    locale: Optional[str] = payload_field(default=None)
    coords: Optional[WitContextCoords] = payload_field(default=None)


@dataclass
class WitMessageMeaningRequest(Payload):
    q: str = payload_field()
    n: int = payload_field(default=1)
    tag: Optional[str] = payload_field(default=None)
    context: Optional[WitContext] = payload_field(default=None)


@dataclass
class WitIntent(Payload):
    id: str = payload_field()
    name: str = payload_field()
    confidence: Real = payload_field()


@dataclass
class WitMessageMeaningResponse(Payload):
    text: str = payload_field()
    entities: dict = payload_field()
    traits: dict = payload_field()
    intents: List[WitIntent] = payload_field()
