from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from meya.salesforce.knowledge.payload.article import (
    SalesforceKnowledgeArticle,
)
from meya.util.enum import SimpleEnum
from typing import List
from typing import Optional


@dataclass
class SalesforceKnowledgeChannel(SimpleEnum):
    APP = "App"
    PKB = "Pkb"
    CSP = "Csp"
    PRM = "Prm"


@dataclass
class SalesforceKnowledgeOrder(SimpleEnum):
    ASC = "ASC"
    DESC = "DESC"


@dataclass
class SalesforceKnowledgeSort(SimpleEnum):
    LAST_PUBLISHED_DATE = "LastPublishedDate"
    CREATED_DATE = "CreatedDate"
    TITLE = "Title"
    VIEW_SCORE = "ViewScore"


@dataclass
class SalesforceKnowledgeSearchRequest(Payload):
    q: str = payload_field()
    page_size: Optional[int] = payload_field(default=None)
    page_number: Optional[int] = payload_field(default=None)
    channel: Optional[SalesforceKnowledgeChannel] = payload_field(default=None)
    order: Optional[SalesforceKnowledgeOrder] = payload_field(default=None)
    sort: Optional[SalesforceKnowledgeSort] = payload_field(default=None)


@dataclass
class SalesforceKnowledgeSearchResponse(Payload):
    to_camel_case_fields = True
    current_page_url: str = payload_field()
    page_number: int = payload_field()
    articles: List[SalesforceKnowledgeArticle] = payload_field(
        default_factory=list
    )
    next_page_url: Optional[str] = payload_field(default=None)
