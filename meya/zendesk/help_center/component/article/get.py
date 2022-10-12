from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.integration.element.api import ApiComponentResponse
from meya.zendesk.help_center.integration import (
    ZendeskHelpCenterIntegrationRef,
)
from meya.zendesk.help_center.payload.article import ZendeskHelpCenterArticle
from typing import Optional


@dataclass
class ZendeskHelpCenterGetArticleComponentResponse(ApiComponentResponse):
    result: ZendeskHelpCenterArticle = response_field(sensitive=True)


@dataclass
class ZendeskHelpCenterGetArticleComponent(BaseApiComponent):
    article_id: int = element_field(
        help="Zendesk help center article unique id"
    )
    locale: Optional[str] = element_field(default=None)
    integration: ZendeskHelpCenterIntegrationRef = element_field()
