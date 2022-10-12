from dataclasses import dataclass
from meya.http.payload import Payload
from typing import ClassVar


@dataclass
class TwilioPayload(Payload):
    to_camel_case_fields: ClassVar[bool] = True
    from_camel_case_fields: ClassVar[bool] = True
