from dataclasses import dataclass
from meya.util.dict import from_dict
from typing import Optional


@dataclass
class TwilioLookupPhone:
    caller_name: Optional[str]
    country_code: str
    phone_number: str
    national_format: str
    carrier: Optional[dict]
    add_ons: Optional[dict]
    url: str

    @staticmethod
    def from_dict(data: dict) -> "TwilioLookupPhone":
        return from_dict(TwilioLookupPhone, data)
