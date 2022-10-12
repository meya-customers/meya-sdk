from dataclasses import dataclass
from meya.element import Element
from meya.element.field import element_field
from meya.salesforce.knowledge.integration import (
    SalesforceKnowledgeIntegrationRef,
)
from meya.salesforce.knowledge.payload.search import SalesforceKnowledgeChannel
from meya.salesforce.knowledge.payload.search import SalesforceKnowledgeOrder
from meya.salesforce.knowledge.payload.search import SalesforceKnowledgeSort
from typing import Optional


@dataclass
class SalesforceKnowledgeMixin(Element):
    locale: str = element_field(
        default="en-US",
        help=(
            "The locale of the articles to be retrieved. "
            "Usually this should be set to the user's locale."
        ),
    )
    page_size: Optional[int] = element_field(
        default=None,
        help="The maximum number of returned articles to be returned.",
    )
    page_number: Optional[int] = element_field(
        default=None,
        help=(
            "The specific page number to retrieve when a search query is "
            "broken up into multiple pages of articles. "
            "This allows you to page through the list of articles."
        ),
    )
    channel: Optional[SalesforceKnowledgeChannel] = element_field(
        default=None,
        help=(
            "Gives the possibility to select different scopes depending on "
            "the situation."
        ),
    )
    order: Optional[SalesforceKnowledgeOrder] = element_field(
        default=None, help="Articles ordering, 'ASC' or 'DESC'."
    )
    sort: Optional[SalesforceKnowledgeSort] = element_field(
        default=None, help="Articles sort."
    )
    article_body_field_name: Optional[str] = element_field(
        default=None,
        help=(
            "This is the specific field name you set in Salesforce to contain "
            "the body of an article. "
            "When this is set, the api will automatically fetch all body "
            "content for a list of articles in a search result. "
            "However, if it's not defined then the api will NOT fetch the "
            "article body content."
        ),
    )
    integration: SalesforceKnowledgeIntegrationRef = element_field()
