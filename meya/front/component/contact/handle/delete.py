from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.front.element.mixin.contact.handle import FrontHandleMixin


@dataclass
class FrontContactHandleDeleteComponentResponse:
    ok: bool = response_field(sensitive=True)


@dataclass
class FrontContactHandleDeleteComponent(BaseApiComponent, FrontHandleMixin):
    force: bool = element_field(
        default=False,
        help=(
            "Setting force to true will delete the contact if the handle to "
            "delete is the last one of the contact"
        ),
    )
