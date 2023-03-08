from dataclasses import dataclass
from meya.component.element.interactive import InteractiveComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.openai.integration.integration import OpenaiIntegrationRef
from meya.util.enum import SimpleEnum
from typing import List
from typing import Optional


class OpenaiQuestionError(SimpleEnum):
    TIMEOUT = "timeout"
    NO_CONTENT = "no_content"
    INTERNAL = "internal"


@dataclass
class OpenaiQuestionComponentResponse:
    error: Optional[OpenaiQuestionError] = response_field(default=None)
    answer: Optional[str] = response_field(default=None)
    sources: Optional[List[str]] = response_field(default=None)


@dataclass
class OpenaiQuestionComponent(InteractiveComponent):
    integration: OpenaiIntegrationRef = element_field(
        help=(
            "Reference path to the OpenAi integration element to use for this "
            "question/answer response."
        )
    )
    question: str = element_field(
        signature=True,
        help="The question text that is being asked.",
    )
    max_tokens: Optional[int] = element_field(
        help=(
            "The maximum number of tokens to generate in the completion."
            "The token count of your prompt plus max_tokens cannot exceed the "
            "model's context length. Most models have a context length of "
            "2048 tokens (except for the newest models, which support 4096)."
            "The question text that is being asked."
        ),
        default=250,
    )
    min_content_chunks: Optional[int] = element_field(
        help=(
            "The minimum number of chunks to include in the prompt template "
            "context."
        ),
        default=2,
    )
    max_content_chunks: Optional[int] = element_field(
        help=(
            "The maximum number of chunks to return from the content index "
            "that are most similar to the given question. The more chunks "
            "added to the context the better the response will be.\n"
            "Note that this is dependent on the chunk size, and chunks will "
            "be automatically truncated to fit within the model's maximum "
            "token limit."
        ),
        default=5,
    )
    min_event_history: Optional[int] = element_field(
        help=(
            "The minimum number of say events to include in the prompt"
            "template context."
        ),
        default=2,
    )
    max_event_history: Optional[int] = element_field(
        help=(
            "The maximum number of say events to return from the event "
            "history to include in the prompt template context.\n"
            "For GPT-3.5 chat models, the event history is automatically "
            "prepended to the prompt's messages. Set this to 0 to disable.\n"
            "Note that the event history will automatically be truncated to "
            "fit within the model's maximum token limit."
        ),
        default=20,
    )
