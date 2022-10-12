from dataclasses import dataclass
from meya.element.field import element_field
from meya.front.element.mixin.contact.base import FrontContactBase
from typing import Optional


@dataclass
class FrontHandleMixin(FrontContactBase):
    contact_id: Optional[str] = element_field(
        default=None, help="The Front Contact ID"
    )
    handle: str = element_field(
        help=(
            "A human readable alias for the Front contact. The format is "
            "alt:<source>:<handle> (e.g. alt:phone:+12345678900)"
        )
    )
