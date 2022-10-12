from dataclasses import dataclass
from meya.component.element.base_api import BaseApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.integration.element.api import ApiComponentResponse
from meya.twilio.integration.base import TwilioBaseIntegrationRef
from meya.twilio.payload.lookup import TwilioLookupPhone
from typing import Optional


@dataclass
class TwilioLookupComponentResponse(ApiComponentResponse):
    result: Optional[TwilioLookupPhone] = response_field()
    data: Optional[dict] = response_field()


@dataclass
class TwilioLookupComponent(BaseApiComponent):
    """
    Learn more: https://www.twilio.com/docs/lookup/api
    """

    phone_number: str = element_field()
    integration: TwilioBaseIntegrationRef = element_field()
