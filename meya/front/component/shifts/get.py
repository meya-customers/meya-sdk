from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.front.element.mixin.base import FrontMixin
from meya.front.payload.shifts import FrontShift
from typing import Optional


@dataclass
class FrontShiftGetComponentResponse:
    result: FrontShift = response_field(sensitive=True)
    ok: bool = response_field(default=True)


@dataclass
class FrontShiftGetComponent(BaseApiComponent, FrontMixin):
    shift_id: Optional[str] = element_field(
        help=(
            "The Front ID of the shift to retrieve. "
            "Shift IDs have the format shf_xxx"
        )
    )
