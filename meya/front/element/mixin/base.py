from dataclasses import dataclass
from meya.element import Element
from meya.element.field import element_field
from meya.front.integration import FrontIntegrationRef


@dataclass
class FrontMixin(Element):
    integration: FrontIntegrationRef = element_field(
        help=(
            "A string identifier for the Front integration "
            "(e.g. integration.front)"
        )
    )
