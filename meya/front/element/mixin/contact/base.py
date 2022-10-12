from dataclasses import dataclass
from meya.element.field import element_field
from meya.front.element.mixin.base import FrontMixin
from meya.front.payload.contact import FrontSource
from typing import Optional


@dataclass
class FrontContactBase(FrontMixin):
    handle: Optional[str] = element_field(
        default=None,
        help=(
            "A human readable alias for the Front contact. The format is "
            "alt:<source>:<handle> (e.g. alt:phone:+12345678900)"
        ),
    )
    source: FrontSource = element_field(
        default=FrontSource.CUSTOM,
        help=(
            "Front contact source. e.g. `email`. "
            "Front enforces contact handle format depending on the contact "
            "source, e.g., for Twitter the contact handle must start with `@` "
            "This value will only be used in case of contact creation."
        ),
    )
