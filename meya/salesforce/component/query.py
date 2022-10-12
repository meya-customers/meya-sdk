from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.integration.element.api import ApiComponentResponse
from meya.salesforce.integration import SalesforceIntegrationRef
from meya.salesforce.payload.query import SalesforceQueryResponse


@dataclass
class SalesforceQueryComponentResponse(ApiComponentResponse):
    result: SalesforceQueryResponse = response_field(sensitive=True)


@dataclass
class SalesforceQueryComponent(BaseApiComponent):
    soql_query: str = element_field(
        help=(
            "Salesforce Object Query Language (SOQL) query string. "
            "Check https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/sforce_api_calls_soql.htm "
            "for more details."
        )
    )
    integration: SalesforceIntegrationRef = element_field()
