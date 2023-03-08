from dataclasses import dataclass
from dataclasses import field
from meya.util.dict import from_dict
from meya.util.dict import to_dict
from typing import Dict
from typing import List
from typing import Optional
from typing import Union


@dataclass
class OpenaiTextHyperparameters:
    suffix: Optional[str] = field(default=None)
    max_tokens: Optional[int] = field(default=None)
    temperature: float = field(default=0.7)
    top_p: float = field(default=1.0)
    n: int = field(default=1)
    logprobs: Optional[int] = field(default=None)
    echo: Optional[bool] = field(default=None)
    stop: Optional[Union[str, List[str]]] = field(default=None)
    presence_penalty: Optional[float] = field(default=None)
    frequency_penalty: Optional[float] = field(default=None)
    best_of: Optional[int] = field(default=None)
    logit_bias: Optional[Dict[str, float]] = field(default=None)

    @classmethod
    def from_dict(
        cls, data: dict, from_camel_case_fields: bool = False
    ) -> "OpenaiTextHyperparameters":
        return from_dict(
            cls,
            data,
            from_camel_case_fields=from_camel_case_fields,
        )

    def to_dict(self) -> dict:
        return to_dict(self)
