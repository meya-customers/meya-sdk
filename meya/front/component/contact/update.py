from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.front.element.mixin.contact import FrontContactMixin
from meya.front.payload.contact import FrontContactUpdateResponse
from typing import Optional


@dataclass
class FrontContactUpdateComponentResponse:
    result: Optional[FrontContactUpdateResponse] = response_field(
        sensitive=True, default=None
    )
    ok: bool = response_field(default=True)


@dataclass
class FrontContactUpdateComponent(BaseApiComponent, FrontContactMixin):
    contact_id: Optional[str] = element_field(
        default=None, help="The Front Contact ID"
    )
