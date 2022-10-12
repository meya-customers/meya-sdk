from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.front.element.mixin.contact import FrontContactMixin
from meya.front.payload.contact import FrontContactCreateOrUpdate
from typing import Optional


@dataclass
class FrontContactCreateOrUpdateComponentResponse:
    result: FrontContactCreateOrUpdate = response_field(sensitive=True)
    ok: bool = response_field(default=True)


@dataclass
class FrontContactCreateOrUpdateComponent(BaseApiComponent, FrontContactMixin):
    contact_id: Optional[str] = element_field(
        default=None, help="The Front Contact ID"
    )
    link: bool = element_field(
        default=True,
        help="Link the current Meya user to this integration user",
    )
