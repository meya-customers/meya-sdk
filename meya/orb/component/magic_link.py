from dataclasses import dataclass
from datetime import timedelta
from meya.component.element import Component
from meya.element.field import element_field
from meya.orb.integration import OrbIntegrationRef
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union


@dataclass
class OrbMagicLinkComponent(Component):
    @dataclass
    class Response:
        result: str
        button_id: Optional[str]

    magic_link: str = element_field(signature=True)
    integration: OrbIntegrationRef = element_field()
    integration_user_id: Optional[str] = element_field(default=None)
    integration_thread_id: Optional[str] = element_field(default=None)
    button_id: Union[str, bool] = element_field()
    single_use: bool = element_field()
    expiry: timedelta = element_field(default=timedelta(hours=24))
