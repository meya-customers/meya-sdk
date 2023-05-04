from dataclasses import dataclass
from meya.element import Element
from meya.element.field import element_field
from meya.zendesk.support.integration import ZendeskSupportIntegrationRef


@dataclass
class ZendeskBaseMixin(Element):
    integration: ZendeskSupportIntegrationRef = element_field(
        help=(
            "The reference path to the Zendesk Support integration file. "
            "See the [integration reference paths](https://docs.meya.ai/docs/integrations-1#integration-reference-paths) "
            "documentation for more information."
        ),
    )
