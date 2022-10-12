from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.integration.element.api import ApiComponentResponse
from meya.salesforce.knowledge.integration import (
    SalesforceKnowledgeIntegrationRef,
)
from meya.salesforce.knowledge.payload.article import (
    SalesforceKnowledgeArticleDetails,
)


@dataclass
class SalesforceKnowledgeGetArticleComponentResponse(ApiComponentResponse):
    result: SalesforceKnowledgeArticleDetails = response_field(sensitive=True)


@dataclass
class SalesforceKnowledgeGetArticleComponent(BaseApiComponent):
    article_id: str = element_field(
        help=(
            "The unique ID of the Salesforce Knowledge article you would like "
            "to get."
        )
    )
    locale: str = element_field(
        default="en-US",
        help=(
            "The locale of the article you would like to get. Usually you "
            "would set this to the user's locale stored in user scope."
        ),
    )
    integration: SalesforceKnowledgeIntegrationRef = element_field()
