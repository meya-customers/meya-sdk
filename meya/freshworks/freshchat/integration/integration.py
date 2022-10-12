from dataclasses import dataclass
from dataclasses import field
from meya.csp.integration import CspIntegration
from meya.db.view.thread import ThreadMode
from meya.element.field import element_field
from meya.freshworks.freshchat.payload.agent import FreshchatAvatar
from typing import ClassVar
from typing import List
from typing import Optional


@dataclass
class FreshchatProperty:
    name: str
    value: str


@dataclass
class FreshchatUser:
    id: Optional[str] = field(default=None)
    created_time: Optional[str] = field(default=None)
    email: Optional[str] = field(default=None)
    avatar: Optional[FreshchatAvatar] = field(default=None)
    phone: Optional[str] = field(default=None)
    properties: Optional[List[FreshchatProperty]] = field(default=None)
    first_name: Optional[str] = field(default=None)
    last_name: Optional[str] = field(default=None)


@dataclass
class FreshchatAssignmentRules:
    no_assignee: Optional[ThreadMode] = field(default=ThreadMode.BOT)
    human_agent: Optional[ThreadMode] = field(default=ThreadMode.AGENT)
    bot_agent: Optional[ThreadMode] = field(default=ThreadMode.BOT)
    group: Optional[ThreadMode] = field(default=ThreadMode.AGENT)


@dataclass
class FreshchatConversationConfig:
    user: Optional[FreshchatUser]
    assign_to_agent: Optional[str]
    assign_to_group: Optional[str]


@dataclass
class FreshchatIntegration(CspIntegration):
    NAME: ClassVar[str] = "freshchat"

    api_token: str = element_field()
    app_id: str = element_field()
    bot_agent_email: str = element_field()
    api_root: str = element_field(default="https://api.freshchat.com")
    channel_name: str = element_field(default="Inbox")
    channel_tags: Optional[List[str]] = element_field(default=None)
    note_indicator: str = element_field(default="📝")
    agent_command_prefix: str = element_field(default="~")
    assignment_rules: FreshchatAssignmentRules = element_field(
        default_factory=FreshchatAssignmentRules
    )
    user_source_property_name: str = element_field(default="source")
    user_source_property_value: str = element_field(default="meya")
