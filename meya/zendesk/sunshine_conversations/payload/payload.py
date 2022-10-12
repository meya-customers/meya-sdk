from dataclasses import dataclass
from meya.http.payload import Payload
from meya.util.dict import from_dict
from meya.util.dict import to_dict
from typing import Any
from typing import Dict


@dataclass
class SunshinePayload(Payload):
    def to_dict(self) -> Dict[str, Any]:
        return to_dict(self, preserve_nones=False, to_camel_case_fields=True)

    @classmethod
    def from_dict(cls, payload_dict: Dict[str, Any]) -> "SunshinePayload":
        return from_dict(cls, payload_dict, from_camel_case_fields=True)
