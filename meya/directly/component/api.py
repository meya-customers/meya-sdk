from dataclasses import dataclass
from meya.component.element.api import ApiComponent
from meya.directly.integration import DirectlyIntegration
from meya.directly.integration import DirectlyIntegrationRef
from meya.directly.integration.api import ApiVersion
from meya.directly.integration.api import DirectlyApi
from meya.element.field import element_field
from meya.element.field import process_field
from meya.entry import Entry
from typing import List


@dataclass
class DirectlyApiComponent(ApiComponent):
    integration: DirectlyIntegrationRef = element_field()
    integration_obj: DirectlyIntegration = process_field()

    async def start(self) -> List[Entry]:
        self.integration_obj = await self.resolve(self.integration)
        return await super().start()

    @property
    def api(self) -> DirectlyApi:
        return self.integration_obj.api

    def get_api(self, version: ApiVersion) -> DirectlyApi:
        return self.integration_obj.get_api(version)

    async def get_conversation_id(self) -> str:
        return await self.thread.reverse_lookup(
            integration_id=self.integration_obj.id
        )

    async def get_user_ref_id(self) -> str:
        return await self.user.reverse_lookup(
            integration_id=self.integration_obj.id
        )
