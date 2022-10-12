from dataclasses import dataclass
from meya.front.payload import FrontPayload
from meya.http.payload.field import payload_field
from typing import List
from typing import Optional


@dataclass
class FrontShiftTimesRange(FrontPayload):
    start: Optional[str] = payload_field(default=None)
    end: Optional[str] = payload_field(default=None)


@dataclass
class FrontShiftTimes(FrontPayload):
    mon: Optional[FrontShiftTimesRange] = payload_field(default=None)
    tue: Optional[FrontShiftTimesRange] = payload_field(default=None)
    wed: Optional[FrontShiftTimesRange] = payload_field(default=None)
    thu: Optional[FrontShiftTimesRange] = payload_field(default=None)
    fri: Optional[FrontShiftTimesRange] = payload_field(default=None)
    sat: Optional[FrontShiftTimesRange] = payload_field(default=None)
    sun: Optional[FrontShiftTimesRange] = payload_field(default=None)


@dataclass
class FrontShift(FrontPayload):
    id: str = payload_field()
    name: str = payload_field()
    color: str = payload_field()
    timezone: str = payload_field()
    times: FrontShiftTimes = payload_field()
    created_at: float = payload_field()
    updated_at: Optional[float] = payload_field(default=None)


@dataclass
class FrontShifts(FrontPayload):
    results: List[FrontShift] = payload_field(
        default_factory=list, key="_results"
    )
