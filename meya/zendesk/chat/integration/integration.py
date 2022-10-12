from dataclasses import dataclass
from meya.csp.integration import CspIntegration
from meya.element import Element
from meya.element import Ref
from meya.element.field import element_field
from meya.integration.element.element import FilterElementSpecUnion
from meya.integration.element.element import IntegrationFilter
from typing import ClassVar
from typing import Type

DEFAULT_TX_GRIDQL = """
meya.event.entry.interactive
OR meya.csp.event
OR meya.button.event.click
OR meya.form.event.submit
OR meya.presence.event.typing
"""


@dataclass
class ZendeskChatIntegrationFilter(IntegrationFilter):
    tx: FilterElementSpecUnion = element_field(default=DEFAULT_TX_GRIDQL)


@dataclass
class ZendeskChatIntegration(CspIntegration):
    NAME: ClassVar[str] = "zendesk_chat"

    account_key: str = element_field()
    agent_command_prefix: str = element_field(default="~")
    filter: IntegrationFilter = element_field(
        default_factory=ZendeskChatIntegrationFilter
    )


class ZendeskChatIntegrationRef(Ref):
    element_type: ClassVar[Type[Element]] = ZendeskChatIntegration
