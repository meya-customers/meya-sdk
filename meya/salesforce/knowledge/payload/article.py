from dataclasses import dataclass
from meya.http.payload import Payload
from meya.http.payload.field import payload_field
from typing import List
from typing import Optional
from typing import Union


@dataclass
class SalesforceKnowledgeArticle(Payload):
    to_camel_case_fields = True
    id: str = payload_field()
    title: str = payload_field()
    url: str = payload_field()
    down_vote_count: int = payload_field()
    view_count: int = payload_field()
    view_score: float = payload_field()
    article_number: str = payload_field()
    category_groups: List[dict] = payload_field(default_factory=list)
    last_published_date: str = payload_field()
    summary: Optional[str] = payload_field(default=None)
    body: Optional[str] = payload_field(default=None)
    url_name: Optional[str] = payload_field(default=None)
    up_vote_count: Optional[int] = payload_field(default=None)


@dataclass
class SalesforceKnowledgeLayoutItems(Payload):
    label: str = payload_field()
    name: str = payload_field()
    type: str = payload_field()
    value: Optional[str] = payload_field(default=None)


@dataclass
class SalesforceKnowledgeArticleDetails(Payload):
    to_camel_case_fields = True
    id: str = payload_field()
    all_view_count: int = payload_field()
    all_view_score: float = payload_field()
    app_down_vote_count: int = payload_field()
    app_up_vote_count: int = payload_field()
    app_view_count: int = payload_field()
    app_view_score: float = payload_field()
    article_number: str = payload_field()
    article_type: str = payload_field()
    category_groups: List[dict] = payload_field(default_factory=list)
    created_by: dict = payload_field()
    created_date: str = payload_field()
    csp_down_vote_count: int = payload_field()
    csp_up_vote_count: int = payload_field()
    csp_view_count: int = payload_field()
    csp_view_score: float = payload_field()
    last_modified_by: dict = payload_field()
    last_modified_date: str = payload_field()
    last_published_date: str = payload_field()
    layout_items: List[SalesforceKnowledgeLayoutItems] = payload_field(
        default_factory=list
    )
    pkb_down_vote_count: int = payload_field()
    pkb_up_vote_count: int = payload_field()
    pkb_view_count: int = payload_field()
    pkb_view_score: float = payload_field()
    prm_down_vote_count: int = payload_field()
    prm_up_vote_count: int = payload_field()
    prm_view_count: int = payload_field()
    prm_view_score: float = payload_field()
    title: str = payload_field()
    url: str = payload_field()
    url_name: str = payload_field()
    version_number: int = payload_field()
    summary: Optional[str] = payload_field(default=None)

    def body(self, article_body_field_name: str) -> Union[None, str]:
        for layout_item in self.layout_items:
            if layout_item.name == article_body_field_name:
                return layout_item.value
