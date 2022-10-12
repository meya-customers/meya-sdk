from dataclasses import dataclass
from meya.element.field import element_field
from meya.element.field import response_field
from meya.salesforce.knowledge.element.mixin import SalesforceKnowledgeMixin
from meya.salesforce.knowledge.payload.search import (
    SalesforceKnowledgeSearchResponse,
)
from meya.text.trigger import TextTrigger
from meya.util.enum import SimpleEnum
from typing import Optional


@dataclass
class SalesforceKnowledgeTriggerResponse:
    search_query: str = response_field(sensitive=True)
    salesforce_knowledge_response: SalesforceKnowledgeSearchResponse = (
        response_field(sensitive=True)
    )


class Expect(SimpleEnum):
    SalesforceKnowledge = "salesforce_knowledge"


@dataclass
class SalesforceKnowledgeTrigger(TextTrigger, SalesforceKnowledgeMixin):
    expect: Optional[Expect] = element_field(signature=True, default=None)
