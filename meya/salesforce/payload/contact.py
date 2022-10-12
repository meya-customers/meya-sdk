from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from meya.salesforce.payload import SalesforceCreateObjectBaseResponse
from typing import Optional


@dataclass
class SalesforceContact(Payload):
    first_name: str = payload_field(key="FirstName")
    last_name: str = payload_field(key="LastName")
    email: Optional[str] = payload_field(default=None, key="Email")
    mobile_phone: Optional[str] = payload_field(
        default=None, key="MobilePhone"
    )
    phone: Optional[str] = payload_field(default=None, key="Phone")
    title: Optional[str] = payload_field(default=None, key="Title")


@dataclass
class SalesforceCreateContactResponse(SalesforceCreateObjectBaseResponse):
    pass


@dataclass
class SalesforceUpdateContactResponse(SalesforceCreateObjectBaseResponse):
    pass
