from dataclasses import dataclass
from http import HTTPStatus
from meya.element.field import meta_field
from meya.entry import Entry
from meya.http.direction import Direction
from meya.integration.element import Integration
from meya.integration.element import IntegrationRef
from typing import ClassVar
from typing import List


@dataclass
class CatchallIntegration(Integration):
    NAME: ClassVar[str] = "catchall"

    run_in_app_container: bool = meta_field(value=True)

    async def accept(self) -> bool:
        if not await super(Integration, Integration).accept(self):
            return False
        elif not self.is_rx:
            return False
        elif self.request.direction == Direction.TX:
            return False
        else:
            return True

    async def process(
        self,
    ) -> List[Entry]:
        refs = [
            ref.ref
            for ref in self.spec_registry.find_top_level_refs(IntegrationRef)
        ]
        if self.request.integration_id not in refs:
            return self.respond(
                status=HTTPStatus.NOT_FOUND,
                data=dict(ok=False, reason="Integration not found."),
            )
        else:
            return []
