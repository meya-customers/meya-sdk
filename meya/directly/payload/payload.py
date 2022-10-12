import json

from dataclasses import MISSING
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from meya.http.payload import Payload
from typing import ClassVar
from typing import List
from typing import Optional
from typing import Type
from typing import Union


def webhook_field(*, default=MISSING, **metadata):
    return field(default=default, metadata=metadata)


def get_optional_type(cls: Type) -> Type:
    """Return the type of Optional[Field]"""
    return (
        getattr(cls, "__args__")
        if getattr(cls, "__origin__", None) is Union
        else (cls,)
    )[0]


@dataclass
class DirectlyPayload(Payload):
    @classmethod
    def dump_schema(cls) -> str:
        return cls._dump_schema(cls.create_schema())

    @classmethod
    def create_schema(cls, stack: List[str] = None) -> dict:
        """
        Recursive method that will construct a schema dictionnary
        by reflecting on the dataclass fields and metadata to be
        used to register dynamic webhooks on Directly Help Desk
        """
        schema = dict()
        stack = stack or list()
        for name, _field in getattr(cls, "__dataclass_fields__").items():
            new_stack = stack + [_field.metadata.get("template") or name]
            type_ = get_optional_type(_field.type)
            try:
                # handle ClassVar type_ that raise an exception
                issubclass(type_, DirectlyPayload)
            except TypeError:
                continue
            if issubclass(type_, DirectlyPayload):
                schema[name] = type_.create_schema(stack=new_stack)
            else:
                if issubclass(type_, (str, Enum)):
                    quote = '"'
                else:
                    quote = ""
                schema[name] = f"{quote}{{{{{'.'.join(new_stack)}}}}}{quote}"
        return schema

    @staticmethod
    def _dump_schema(schema: dict) -> str:
        """
        Converts a schema dict into a JSON-like string that can be pasted
        into Directly Help Desk webhooks.
        """
        string = json.dumps(schema, indent=True)
        replaces = [(' "{', " {"), ('}}"', "}}"), ('"\\', ""), ('\\"', "")]
        for before, after in replaces:
            string = string.replace(before, after)
        return string


@dataclass
class Question(DirectlyPayload):
    uuid: str = webhook_field()
    timestamp: int = webhook_field(template="date_created.time_ms")
    subject: str = webhook_field()
    text: str = webhook_field()


@dataclass
class Author(DirectlyPayload):
    uuid: str = webhook_field()
    name: str = webhook_field()
    avatar: str = webhook_field()


@dataclass
class Expert(Author):
    pass


@dataclass
class CommentAuthor(Author):
    is_poster: Optional[bool] = webhook_field()
    is_chatbot: Optional[bool] = webhook_field()

    @property
    def is_expert(self) -> bool:
        return not self.is_poster and not self.is_chatbot


@dataclass
class Comment(DirectlyPayload):
    uuid: str = webhook_field()
    timestamp: int = webhook_field(template="date_created.time_ms")
    text: str = webhook_field()
    is_auto_answer: Optional[bool] = webhook_field()
    author: CommentAuthor = webhook_field()

    @property
    def author_uuid(self) -> Optional[str]:
        if self.author:
            return self.author.uuid
        else:
            return None


@dataclass
class Answer(DirectlyPayload):
    uuid: str = webhook_field()
    timestamp: int = webhook_field(template="date_created.time_ms")
    text: str = webhook_field()
    author: Author = webhook_field()
    expert: Expert = webhook_field()
    comment: Comment = webhook_field()

    @property
    def author_uuid(self) -> Optional[str]:
        if self.comment:
            return self.comment.author_uuid
        elif self.author:
            return self.author.uuid
        else:
            return None


# convenient list of available event type strings (not-exhaustive)
class EventType:
    QUESTION_APPROVED = "QUESTION_APPROVED"
    QUESTION_FIRST_RESPONSE = "QUESTION_FIRST_RESPONSE"
    QUESTION_CATEGORIZED = "QUESTION_CATEGORIZED"
    QUESTION_ESCALATED_BY_EXPERT = "QUESTION_ESCALATED_BY_EXPERT"
    QUESTION_ESCALATED_BY_TIME = "QUESTION_ESCALATED_BY_TIME"
    QUESTION_REJECTED_BY_KEYWORD = "QUESTION_REJECTED_BY_KEYWORD"
    QUESTION_REJECTED_BY_BLOCKED_USER = "QUESTION_REJECTED_BY_BLOCKED_USER"
    QUESTION_REJECTED_BY_PREDICTIVE_ROUTING = (
        "QUESTION_REJECTED_BY_PREDICTIVE_ROUTING"
    )
    QUESTION_EXPIRED = "QUESTION_EXPIRED"
    QUESTION_REJECTED_BY_OPTED_OUT_USER = "QUESTION_REJECTED_BY_OPTED_OUT_USER"
    QUESTION_REJECTED_BY_UNSUBSCRIBED_USER = (
        "QUESTION_REJECTED_BY_UNSUBSCRIBED_USER"
    )
    QUESTION_FLAGGED_EMERGENCY = "QUESTION_FLAGGED_EMERGENCY"
    QUESTION_FLAGGED_PII = "QUESTION_FLAGGED_PII"
    ANSWER_FLAGGED_ABUSE = "ANSWER_FLAGGED_ABUSE"
    QUESTION_RESPONSE = "QUESTION_RESPONSE"
    QUESTION_MARKED_AS_RESOLVED = "QUESTION_MARKED_AS_RESOLVED"
    QUESTION_CLAIMED = "QUESTION_CLAIMED"
    QUESTION_RELEASED = "QUESTION_RELEASED"
    QUESTION_TIMEOUT_WARNING = "QUESTION_TIMEOUT_WARNING"
    QUESTION_CREATED = "QUESTION_CREATED"
    # TODO: verify this string
    QUESTION_UPDATED = "QUESTION_UPDATED"
    QUESTION_FIRST_VIEWED_RESPONSE = "QUESTION_FIRST_VIEWED_RESPONSE"
    QUESTION_ESCALATED_BY_CUSTOMER = "QUESTION_ESCALATED_BY_CUSTOMER"
    QUESTION_RESOLVED = "QUESTION_RESOLVED"
    QUESTION_CLOSED_BY_COMPANY = "QUESTION_CLOSED_BY_COMPANY"
    QUESTION_RATED = "QUESTION_RATED"


@dataclass
class Message(DirectlyPayload):
    uuid: str = webhook_field()
    text: str = webhook_field()


@dataclass
class DirectlyWebhookPayload(DirectlyPayload):
    event_type: str = webhook_field()
    timestamp: int = webhook_field(template="timestamp.time_ms")
    question: Optional[Question] = webhook_field()
    answer: Optional[Answer] = webhook_field()
    message: Optional[Message] = webhook_field()
    extra: Optional[dict] = webhook_field()

    @property
    def is_expert_say(self) -> bool:
        if self.event_type == EventType.QUESTION_RESPONSE:
            return self.answer.comment.author.is_expert
        else:
            return False

    @property
    def is_conversation_terminated(self) -> bool:
        # TODO: expand this set?
        return self.event_type in {
            EventType.QUESTION_FLAGGED_PII,
            EventType.QUESTION_FLAGGED_EMERGENCY,
            EventType.QUESTION_RESOLVED,
        }

    @property
    def timestamp_seconds(self) -> float:
        return self.timestamp / 100

    @property
    def author_uuid(self) -> Optional[str]:
        if self.answer:
            return self.answer.author_uuid
        else:
            return None

    @property
    def is_expert(self) -> bool:
        return self.author_uuid and not self.is_user

    @property
    def is_user(self) -> bool:
        if not self.answer:
            return False
        if not self.answer.comment:
            return False
        return self.answer.comment.author.is_poster

    @property
    def is_system(self) -> bool:
        return not (self.is_expert or self.is_user)

    @property
    def question_uuid(self) -> Optional[str]:
        if self.question:
            return self.question.uuid
        else:
            return None
