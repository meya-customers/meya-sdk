from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.integration.element.api import ApiComponentResponse
from meya.salesforce.knowledge.element.mixin import SalesforceKnowledgeMixin
from meya.salesforce.knowledge.payload.search import (
    SalesforceKnowledgeSearchResponse,
)


@dataclass
class SalesforceKnowledgeSearchComponentResponse(ApiComponentResponse):
    result: SalesforceKnowledgeSearchResponse = response_field(sensitive=True)


@dataclass
class SalesforceKnowledgeSearchComponent(
    BaseApiComponent, SalesforceKnowledgeMixin
):
    soql_query: str = element_field(
        help=(
            "Salesforce Object Query Language (SOQL) query string. "
            "Check https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm "
            "for more details."
        )
    )
