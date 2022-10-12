from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.front.element.mixin.base import FrontMixin
from meya.front.payload.teams import FrontTeam
from typing import Optional


@dataclass
class FrontTeamsGetComponentResponse:
    result: FrontTeam = response_field(sensitive=True)
    ok: bool = response_field(default=True)


@dataclass
class FrontTeamsGetComponent(BaseApiComponent, FrontMixin):
    team_id: Optional[str] = element_field(
        help=(
            "The Front ID of the team to retrieve. "
            "Team IDs have the format tim_xxxx"
        )
    )
