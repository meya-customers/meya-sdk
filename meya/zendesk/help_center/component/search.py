from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import response_field
from meya.integration.element.api import ApiComponentResponse
from meya.zendesk.help_center.element.mixin import ZendeskHelpCenterMixin
from meya.zendesk.help_center.payload.query import (
    ZendeskHelpCenterSearchResponse,
)


@dataclass
class ZendeskHelpCenterSearchComponentResponse(ApiComponentResponse):
    result: ZendeskHelpCenterSearchResponse = response_field(sensitive=True)


@dataclass
class ZendeskHelpCenterSearchComponent(
    BaseApiComponent, ZendeskHelpCenterMixin
):
    pass
