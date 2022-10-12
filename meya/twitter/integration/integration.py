from dataclasses import dataclass
from meya.csp.integration import CspIntegration
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from typing import ClassVar
from typing import Type


@dataclass
class TwitterIntegration(CspIntegration):
    NAME: ClassVar[str] = "twitter"
    mark_incoming_as_read: bool = element_field(
        default=True, help="Mark incoming messages from users as read"
    )


class TwitterIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = TwitterIntegration
