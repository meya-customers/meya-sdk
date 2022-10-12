import pytz

from dataclasses import dataclass
from datetime import datetime
from datetime import timedelta
from meya.front.payload import FrontPayload
from meya.front.payload.comment import FrontCommentGet
from meya.front.payload.conversation import FrontConversationGet
from meya.front.payload.message import FrontMessageGet
from meya.front.payload.message import FrontPartnerChannelMessage
from meya.front.payload.message import FrontPartnerChannelMetadata
from meya.front.payload.rules import FrontRule
from meya.front.payload.tag import FrontTagTarget
from meya.front.payload.teammate import FrontTeammateGet
from meya.http.payload.field import payload_field
from meya.time.time import from_utc_seconds_timestamp
from meya.util.enum import SimpleEnum
from numbers import Real
from typing import Any
from typing import Dict
from typing import Optional
from typing import Union


"""
https://dev.frontapp.com/reference/events-1
"""


class FrontSourceTargetMetaType(SimpleEnum):
    TEAMMATE = "teammate"
    RULE = "rule"
    REMINDER = "reminder"
    INBOXES = "inboxes"
    MESSAGE = "message"
    RECIPIENT = "recipient"
    TAG = "tag"
    DELETED_CONVERSATION_IDS = "deleted_conversation_ids"
    COMMENT = "comment"
    API = "api"


@dataclass
class FrontEvent(FrontPayload):
    @classmethod
    def from_typed_dict(
        cls, payload_dict: Dict[str, Any]
    ) -> Optional["FrontEvent"]:
        ALL = {
            "inbound": FrontInboundEvent,
            "outbound": FrontOutboundEvent,
            "out_reply": FrontOutboundEvent,
            "comment": FrontCommentEvent,
            "assign": FrontAssignEvent,
            "unassign": FrontUnassignEvent,
            "message": FrontChannelMessageEvent,
            "tag": FrontTagEvent,
            "untag": FrontUntagEvent,
            "trash": FrontTrashConversationEvent,
            "archive": FrontArchiveConversationEvent,
            "reopen": FrontReopenConversationEvent,
            "restore": FrontRestoreConversationEvent,
        }

        event_subclass = ALL.get(payload_dict["type"])
        if event_subclass:
            return event_subclass.from_dict(payload_dict)
        else:
            return None

    @property
    def is_expired(self) -> bool:
        return False


@dataclass
class FrontActionEvent(FrontEvent):
    conversation: FrontConversationGet = payload_field()
    emitted_at: Real = payload_field()

    @property
    def is_expired(self) -> bool:
        emitted_at_delta = abs(
            datetime.now(pytz.utc)
            - from_utc_seconds_timestamp(self.emitted_at)
        )
        return emitted_at_delta >= timedelta(minutes=5)


@dataclass
class FrontEventMessageData(FrontPayload):
    data: FrontMessageGet = payload_field()


@dataclass
class FrontEventCommentData(FrontPayload):
    data: FrontCommentGet = payload_field()


@dataclass
class FrontSourceTargetMeta(FrontPayload):
    type: FrontSourceTargetMetaType = payload_field()


@dataclass
class FrontSourceTargetData(FrontPayload):
    data: Optional[Union[FrontTeammateGet, FrontRule]] = payload_field(
        default=None
    )
    meta: FrontSourceTargetMeta = payload_field(key="_meta")


@dataclass
class FrontInboundEvent(FrontActionEvent):
    target: FrontEventMessageData = payload_field()


@dataclass
class FrontOutboundEvent(FrontActionEvent):
    target: FrontEventMessageData = payload_field()


@dataclass
class FrontCommentEvent(FrontActionEvent):
    target: FrontEventCommentData = payload_field()


@dataclass
class FrontAssignEvent(FrontActionEvent):
    target: FrontSourceTargetData = payload_field()


@dataclass
class FrontUnassignEvent(FrontActionEvent):
    source: FrontSourceTargetData = payload_field()


@dataclass
class FrontTagEvent(FrontActionEvent):
    target: FrontTagTarget = payload_field()
    source: FrontSourceTargetData = payload_field()


@dataclass
class FrontUntagEvent(FrontActionEvent):
    target: FrontTagTarget = payload_field()
    source: FrontSourceTargetData = payload_field()


@dataclass
class FrontTrashConversationEvent(FrontActionEvent):
    source: FrontSourceTargetData = payload_field()


@dataclass
class FrontArchiveConversationEvent(FrontActionEvent):
    source: FrontSourceTargetData = payload_field()


@dataclass
class FrontReopenConversationEvent(FrontActionEvent):
    source: FrontSourceTargetData = payload_field()


@dataclass
class FrontRestoreConversationEvent(FrontActionEvent):
    source: FrontSourceTargetData = payload_field()


@dataclass
class FrontChannelMessageEvent(FrontEvent):
    payload: FrontPartnerChannelMessage = payload_field()
    metadata: FrontPartnerChannelMetadata = payload_field()

    @property
    def conversation_id(self) -> str:
        return self.payload.links.related.conversation.split("/")[-1]
