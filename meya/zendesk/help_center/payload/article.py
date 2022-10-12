from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from meya.zendesk.help_center.payload import ZendeskHelpCenterBaseResponse
from typing import List
from typing import Optional


@dataclass
class ZendeskHelpCenterArticle(Payload):
    locale: str = payload_field()
    title: str = payload_field()
    author_id: int = payload_field()
    permission_group_id: int = payload_field()
    id: int = payload_field()
    outdated_locales: List[str] = payload_field(default_factory=list)
    vote_sum: int = payload_field()
    vote_count: int = payload_field()
    name: Optional[str] = payload_field(default=None)
    user_segment_id: Optional[int] = payload_field(default=None)
    body: Optional[str] = payload_field(default=None)
    comments_disabled: Optional[bool] = payload_field(default=None)
    created_at: Optional[str] = payload_field(default=None)
    updated_at: Optional[str] = payload_field(default=None)
    draft: Optional[bool] = payload_field(default=None)
    edited_at: Optional[str] = payload_field(default=None)
    html_url: Optional[str] = payload_field(default=None)
    label_names: Optional[List[str]] = payload_field(default=None)
    outdated: Optional[bool] = payload_field(default=None)
    position: Optional[int] = payload_field(default=None)
    promoted: Optional[bool] = payload_field(default=None)
    section_id: Optional[int] = payload_field(default=None)
    source_locale: Optional[str] = payload_field(default=None)
    url: Optional[str] = payload_field(default=None)


@dataclass
class ZendeskHelpCenterArticleAttachment(Payload):
    id: int = payload_field()
    article_id: int = payload_field()
    content_type: str = payload_field()
    content_url: str = payload_field()
    file_name: str = payload_field()
    inline: bool = payload_field()
    size: int = payload_field()
    url: str = payload_field()
    created_at: str = payload_field()
    updated_at: Optional[str] = payload_field(default=None)


@dataclass
class ZendeskHelpCenterArticlesResponse(ZendeskHelpCenterBaseResponse):
    articles: List[ZendeskHelpCenterArticle] = payload_field(
        default_factory=list
    )
