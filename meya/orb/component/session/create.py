from dataclasses import dataclass
from meya.component.element import Component
from meya.element.field import element_field
from meya.orb.integration import OrbIntegrationRef
from typing import Optional


@dataclass
class OrbSessionCreateComponent(Component):
    @dataclass
    class Response:
        integration_user_id: str
        integration_thread_id: str

    integration: OrbIntegrationRef = element_field()
    user_id: Optional[str] = element_field(default=None)
    thread_id: Optional[str] = element_field(default=None)
    integration_user_id: Optional[str] = element_field(default=None)
    integration_thread_id: Optional[str] = element_field(default=None)
