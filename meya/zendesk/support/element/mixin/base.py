from dataclasses import dataclass
from meya.element import Element
from meya.element.field import element_field
from meya.zendesk.support.integration import ZendeskSupportIntegrationRef


@dataclass
class ZendeskBaseMixin(Element):
    integration: ZendeskSupportIntegrationRef = element_field()
