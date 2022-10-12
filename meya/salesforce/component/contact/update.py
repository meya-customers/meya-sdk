from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.integration.element.api import ApiComponentResponse
from meya.salesforce.element.mixin import SalesforceContactMixin
from meya.salesforce.payload.contact import SalesforceUpdateContactResponse
from typing import Optional


@dataclass
class SalesforceContactUpdateResponse(ApiComponentResponse):
    result: SalesforceUpdateContactResponse = response_field(sensitive=True)


@dataclass
class SalesforceContactUpdateComponent(
    BaseApiComponent, SalesforceContactMixin
):
    contact_id: Optional[str] = element_field(default=None)
