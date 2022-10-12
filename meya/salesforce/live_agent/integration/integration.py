from dataclasses import dataclass
from meya.csp.integration import CspIntegration
from meya.element.field import element_field
from meya.integration.element.element import FilterElementSpecUnion
from meya.integration.element.element import IntegrationFilter
from meya.text.markdown import MarkdownElementSpecUnion
from typing import ClassVar

DEFAULT_TX_GRIDQL = """
meya.event.entry.interactive
OR meya.csp.event
OR meya.button.event.click
OR meya.form.event.submit
OR meya.presence.event.typing
"""


@dataclass
class LiveAgentIntegrationFilter(IntegrationFilter):
    tx: FilterElementSpecUnion = element_field(default=DEFAULT_TX_GRIDQL)


@dataclass
class LiveAgentIntegration(CspIntegration):
    NAME: ClassVar[str] = "liveagent"

    api_endpoint: str = element_field()
    organization_id: str = element_field()
    deployment_id: str = element_field()
    button_id: str = element_field()
    note_indicator: str = element_field(default="📝")
    markdown: MarkdownElementSpecUnion = element_field(default=False)
    filter: IntegrationFilter = element_field(
        default_factory=LiveAgentIntegrationFilter
    )
