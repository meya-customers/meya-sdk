from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from meya.util.enum import SimpleEnum
from typing import Optional


class TransactionStatus(SimpleEnum):
    PENDING = "pending"
    FAILURE = "failure"
    SUCCESS = "success"
    ERROR = "error"


class TransactionKind(SimpleEnum):
    AUTHORIZATION = "authorization"
    CAPTURE = "capture"
    SALE = "sale"
    VOID = "void"
    REFUND = "refund"


@dataclass
class Transaction(Payload):
    id: int = payload_field()
    amount: float = payload_field()
    authorization: str = payload_field()
    created_at: str = payload_field()
    currency: str = payload_field()
    device_id: int = payload_field()
    error_code: str = payload_field()
    extended_authorization_attributes: Optional[dict] = payload_field()
    gateway: str = payload_field()
    kind: TransactionKind = payload_field()
    location_id: int = payload_field()
    message: str = payload_field()
    order_id: str = payload_field()
    parent_id: int = payload_field()
    processed_at: str = payload_field()
    source_name: Optional[str] = payload_field()
    status: TransactionStatus = payload_field()
    test: bool = payload_field()
    user_id: int = payload_field()
    currency_exchange_adjustment: Optional[dict] = payload_field(default=None)
    receipt: Optional[dict] = payload_field(default=None)
    payment_details: Optional[dict] = payload_field(default=None)
    authorization_expires_at: Optional[str] = payload_field(default=None)
