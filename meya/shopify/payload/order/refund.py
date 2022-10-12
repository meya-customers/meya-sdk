from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from meya.util.enum import SimpleEnum
from typing import Optional


class ShippingType(SimpleEnum):
    FULL_REFUND = "full_refund"
    AMOUNT = "amount"


class RestockType(SimpleEnum):
    NO_RESTOCK = "no_restock"
    CANCEL = "cancel"
    RETURN = "return"


@dataclass
class RefundLineItem(Payload):
    line_item_id: int = payload_field()
    quantity: float = payload_field()
    restock_type: RestockType = payload_field()
    location_id: Optional[int] = payload_field(default=None)


@dataclass
class RefundBase(Payload):
    refund: dict = payload_field()


@dataclass
class CalculateRefund(RefundBase):
    pass


@dataclass
class RefundResponse(RefundBase):
    pass
