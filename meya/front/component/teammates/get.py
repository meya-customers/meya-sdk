from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.front.element.mixin.base import FrontMixin
from meya.front.payload.teammate import FrontTeammateGet
from typing import Optional


@dataclass
class FrontTeammateGetComponentResponse:
    result: FrontTeammateGet = response_field(sensitive=True)
    ok: bool = response_field(default=True)


@dataclass
class FrontTeammateGetComponent(BaseApiComponent, FrontMixin):
    teammate_id: Optional[str] = element_field(
        help=(
            "The Front ID of the teammate to retrieve. "
            "Teammate IDs have the format tea_xxxx"
        )
    )
