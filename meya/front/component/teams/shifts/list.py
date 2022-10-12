from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.front.element.mixin.base import FrontMixin
from meya.front.payload.shifts import FrontShifts
from meya.integration.element.api import ApiComponentResponse


@dataclass
class FrontTeamShiftsListComponentResponse(ApiComponentResponse):
    result: FrontShifts = response_field(sensitive=True)
    ok: bool = response_field(default=True)


@dataclass
class FrontTeamShiftsListComponent(BaseApiComponent, FrontMixin):
    team_id: str = element_field(
        help=(
            "The Front ID of the team whose shifts you want to retrieve. "
            "Team IDs have the format tim_xxxx"
        )
    )
