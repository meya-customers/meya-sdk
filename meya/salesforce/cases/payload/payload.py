from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from meya.salesforce.payload import SalesforceCreateObjectBaseResponse
from typing import Optional


@dataclass
class SalesforceCaseBase(Payload):
    subject: str = payload_field(key="Subject")
    status: str = payload_field(key="Status")
    comments: Optional[str] = payload_field(default=None, key="Comments")
    closed_date: Optional[str] = payload_field(default=None, key="ClosedDate")
    contact_email: Optional[str] = payload_field(
        default=None, key="ContactEmail"
    )
    contact_fax: Optional[str] = payload_field(default=None, key="ContactFax")
    contact_id: Optional[str] = payload_field(default=None, key="ContactId")
    contact_mobile: Optional[str] = payload_field(
        default=None, key="ContactMobile"
    )
    contact_phone: Optional[str] = payload_field(
        default=None, key="ContactPhone"
    )
    description: Optional[str] = payload_field(default=None, key="Description")
    is_deleted: Optional[bool] = payload_field(default=None, key="IsDeleted")
    is_escalated: Optional[bool] = payload_field(
        default=None, key="IsEscalated"
    )
    last_referenced_date: Optional[str] = payload_field(
        default=None, key="LastReferencedDate"
    )
    last_viewed_date: Optional[str] = payload_field(
        default=None, key="LastViewedDate"
    )
    master_record_id: Optional[str] = payload_field(
        default=None, key="MasterRecordId"
    )
    origin: Optional[str] = payload_field(default=None, key="Origin")
    owner_id: Optional[str] = payload_field(default=None, key="OwnerId")
    parent_id: Optional[str] = payload_field(default=None, key="ParentId")
    priority: Optional[str] = payload_field(default=None, key="Priority")
    reason: Optional[str] = payload_field(default=None, key="Reason")
    source_id: Optional[str] = payload_field(default=None, key="SourceId")
    supplied_company: Optional[str] = payload_field(
        default=None, key="SuppliedCompany"
    )
    supplied_email: Optional[str] = payload_field(
        default=None, key="SuppliedEmail"
    )
    supplied_name: Optional[str] = payload_field(
        default=None, key="SuppliedName"
    )
    supplied_phone: Optional[str] = payload_field(
        default=None, key="SuppliedPhone"
    )
    type: Optional[str] = payload_field(default=None, key="Type")


@dataclass
class SalesforceCasesCreateRequest(SalesforceCaseBase):
    account_id: Optional[str] = payload_field(default=None, key="AccountId")


@dataclass
class SalesforceCasesCreateResponse(SalesforceCreateObjectBaseResponse):
    pass


@dataclass
class SalesforceCasesAddCommentResponse(SalesforceCreateObjectBaseResponse):
    pass


@dataclass
class SalesforceCasesUpdateRequest(SalesforceCaseBase):
    pass


@dataclass
class SalesforceCasesUpdateResponse(SalesforceCreateObjectBaseResponse):
    pass
