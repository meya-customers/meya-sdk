from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Union


@dataclass
class OpenaiPayload(Payload):
    preserve_nones: ClassVar[bool] = False


@dataclass
class OpenaiCompletionRequest(OpenaiPayload):
    model: str = payload_field()
    prompt: Union[str, List[str]] = payload_field()
    suffix: Optional[str] = payload_field(default=None)
    max_tokens: Optional[int] = payload_field(default=None)
    temperature: Optional[float] = payload_field(default=None)
    top_p: Optional[float] = payload_field(default=None)
    n: Optional[int] = payload_field(default=None)
    stream: Optional[bool] = payload_field(default=None)
    logprobs: Optional[int] = payload_field(default=None)
    echo: Optional[bool] = payload_field(default=None)
    stop: Optional[Union[str, List[str]]] = payload_field(default=None)
    presence_penalty: Optional[float] = payload_field(default=None)
    frequency_penalty: Optional[float] = payload_field(default=None)
    best_of: Optional[int] = payload_field(default=None)
    logit_bias: Optional[Dict[str, float]] = payload_field(default=None)
    user: Optional[str] = payload_field(default=None)


@dataclass
class OpenaiChatMessage(OpenaiPayload):
    content: str = payload_field()
    role: Optional[str] = payload_field(default=None)
    name: Optional[str] = payload_field(default=None)


@dataclass
class OpenaiChatCompletionRequest(OpenaiPayload):
    model: str = payload_field()
    messages: List[OpenaiChatMessage] = payload_field()
    max_tokens: Optional[int] = payload_field(default=None)
    temperature: Optional[float] = payload_field(default=None)
    top_p: Optional[float] = payload_field(default=None)
    n: Optional[int] = payload_field(default=None)
    stream: Optional[bool] = payload_field(default=None)
    stop: Optional[Union[str, List[str]]] = payload_field(default=None)
    presence_penalty: Optional[float] = payload_field(default=None)
    frequency_penalty: Optional[float] = payload_field(default=None)
    logit_bias: Optional[Dict[str, float]] = payload_field(default=None)
    user: Optional[str] = payload_field(default=None)


@dataclass
class OpenaiChoice(OpenaiPayload):
    text: Optional[str] = payload_field(default=None)
    index: Optional[int] = payload_field(default=None)
    logprobs: Optional[str] = payload_field(default=None)
    finish_reason: Optional[str] = payload_field(default=None)


@dataclass
class OpenaiUsage(OpenaiPayload):
    prompt_tokens: Optional[int] = payload_field(default=None)
    completion_tokens: Optional[int] = payload_field(default=None)
    total_tokens: Optional[int] = payload_field(default=None)


@dataclass
class OpenaiCompletionResponse(OpenaiPayload):
    id: Optional[str] = payload_field(default=None)
    object: Optional[str] = payload_field(default=None)
    created: Optional[int] = payload_field(default=None)
    model: Optional[str] = payload_field(default=None)
    choices: Optional[List[OpenaiChoice]] = payload_field(default=None)
    usage: Optional[OpenaiUsage] = payload_field(default=None)


@dataclass
class OpenaiChatChoice(OpenaiPayload):
    index: Optional[int] = payload_field(default=None)
    message: Optional[OpenaiChatMessage] = payload_field(default=None)
    finish_reason: Optional[str] = payload_field(default=None)


@dataclass
class OpenaiChatCompletionResponse(OpenaiPayload):
    id: Optional[str] = payload_field(default=None)
    object: Optional[str] = payload_field(default=None)
    created: Optional[int] = payload_field(default=None)
    model: Optional[str] = payload_field(default=None)
    choices: Optional[List[OpenaiChatChoice]] = payload_field(default=None)
    usage: Optional[OpenaiUsage] = payload_field(default=None)


@dataclass
class OpenaiEmbeddingRequest(OpenaiPayload):
    model: str = payload_field()
    input: Union[str, List[str]] = payload_field()
    user: Optional[str] = payload_field(default=None)


@dataclass
class OpenaiEmbedding(OpenaiPayload):
    object: Optional[str] = payload_field(default=None)
    embedding: Optional[List[float]] = payload_field(default=None)
    index: Optional[int] = payload_field(default=None)


@dataclass
class OpenaiEmbeddingResponse(OpenaiPayload):
    object: Optional[str] = payload_field(default=None)
    data: Optional[List[OpenaiEmbedding]] = payload_field(default=None)
    model: Optional[str] = payload_field(default=None)
    usage: Optional[OpenaiUsage] = payload_field(default=None)
