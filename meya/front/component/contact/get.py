from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.front.element.mixin.contact.base import FrontContactBase
from meya.front.payload.contact import FrontContactGet
from typing import Optional


@dataclass
class FrontContactGetComponentResponse:
    result: Optional[FrontContactGet] = response_field(
        sensitive=True, default=None
    )
    ok: bool = response_field(default=True)


@dataclass
class FrontContactGetComponent(BaseApiComponent, FrontContactBase):
    contact_id: Optional[str] = element_field(
        default=None, help="Front Contact ID"
    )
