from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import response_field
from meya.front.element.mixin.base import FrontMixin
from meya.front.payload.shifts import FrontShifts


@dataclass
class FrontShiftListComponentResponse:
    result: FrontShifts = response_field(sensitive=True)
    ok: bool = response_field(default=True)


@dataclass
class FrontShiftListComponent(BaseApiComponent, FrontMixin):
    pass
