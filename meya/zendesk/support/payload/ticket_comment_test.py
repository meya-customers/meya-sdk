import pytest

from meya.zendesk.support.payload.attachment import ZendeskSupportAttachment
from meya.zendesk.support.payload.ticket_comment import (
    ZendeskSupportTicketCommentGet,
)
from typing import Any
from typing import Dict
from typing import Optional


@pytest.mark.parametrize(
    ("payload_dict", "payload", "body_with_links"),
    [
        (
            {
                "id": 1220510153033,
                "type": "Comment",
                "author_id": 365491090854,
                "body": "Hello **world**",
                "html_body": '<div class="zd-comment" dir="auto">Hello <b>world</b><br></div>',
                "plain_body": "Hello world",
                "public": True,
                "attachments": [
                    {
                        "url": "https://d3v-meya.zendesk.com/api/v2/attachments/379685468553.json",
                        "id": 379685468553,
                        "file_name": "avataaars.png",
                        "content_url": "https://d3v-meya.zendesk.com/attachments/token/qsUzlGLCuvRMDPDKmRb4FzAIl/?name=avataaars.png",
                        "mapped_content_url": "https://d3v-meya.zendesk.com/attachments/token/qsUzlGLCuvRMDPDKmRb4FzAIl/?name=avataaars.png",
                        "content_type": "image/png",
                        "size": 44372,
                        "width": 528,
                        "height": 560,
                        "inline": False,
                        "deleted": False,
                        "thumbnails": [
                            {
                                "url": "https://d3v-meya.zendesk.com/api/v2/attachments/379685468773.json",
                                "id": 379685468773,
                                "file_name": "avataaars_thumb.png",
                                "content_url": "https://d3v-meya.zendesk.com/attachments/token/HcOlyEEieSgCqzrtOc4acAc42/?name=avataaars_thumb.png",
                                "mapped_content_url": "https://d3v-meya.zendesk.com/attachments/token/HcOlyEEieSgCqzrtOc4acAc42/?name=avataaars_thumb.png",
                                "content_type": "image/png",
                                "size": 6608,
                                "width": 75,
                                "height": 80,
                                "inline": False,
                                "deleted": False,
                            }
                        ],
                    }
                ],
                "audit_id": 1220510152853,
                "via": {
                    "channel": "web",
                    "source": {"from": {}, "to": {}, "rel": None},
                },
                "created_at": "2020-07-15T20:41:52Z",
                "metadata": {
                    "system": {
                        "client": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
                        "ip_address": "108.168.19.134",
                        "location": "Kitchener, ON, Canada",
                        "latitude": 43.4103,
                        "longitude": -80.5038,
                    },
                    "custom": {},
                },
            },
            ZendeskSupportTicketCommentGet(
                attachments=[
                    ZendeskSupportAttachment(
                        id=379685468553,
                        file_name="avataaars.png",
                        content_url="https://d3v-meya.zendesk.com/attachments/token/qsUzlGLCuvRMDPDKmRb4FzAIl/?name=avataaars.png",
                        content_type="image/png",
                    )
                ],
                author_id=365491090854,
                body="Hello **world**",
                created_at="2020-07-15T20:41:52Z",
                html_body='<div class="zd-comment" dir="auto">Hello <b>world</b><br></div>',
                id=1220510153033,
                public=True,
            ),
            None,
        ),
        (
            {
                "id": 1226851718033,
                "type": "Comment",
                "author_id": 114318908893,
                "body": "# H1\n\n## H2\n\n### H3\n\n#### H4\n\n##### H5\nNormal\n**Bold**\n**_BoldItalic_**\n_Italic_\n\n- Bullet1\n- Bullet2\n\n1. Number1\n2. Number2\n\n\nIndent\n\n\n\n> Quote\n\n\n`Code span`\n\n\n    Code block",
                "html_body": '<div class="zd-comment" dir="auto"><h1 dir="auto">H1</h1><h2 dir="auto">H2</h2><h3 dir="auto">H3</h3><h4 dir="auto">H4</h4><h5 dir="auto">H5</h5>Normal<br><b>Bold</b><br><b><i>BoldItalic</i></b><br><i>Italic</i><br><ul dir="auto"><li>Bullet1</li><li>Bullet2</li></ul><ol dir="auto"><li>Number1</li><li>Number2</li></ol><br><div style="margin-left: 20px"><p dir="auto">Indent</p></div><br><blockquote><p dir="auto">Quote</p></blockquote><br><code>Code span</code><br><br><pre style="white-space: pre-wrap">Code block<br></pre><br></div>',
                "plain_body": "H1  H2  H3  H4  H5 Normal\nBold\nBoldItalic\nItalic\n  Bullet1  Bullet2    Number1  Number2  \n  Indent  \n  Quote  \nCode span\n\n Code block",
                "public": True,
                "attachments": [],
                "audit_id": 1226851717853,
                "via": {
                    "channel": "web",
                    "source": {"from": {}, "to": {}, "rel": None},
                },
                "created_at": "2020-07-21T15:27:14Z",
                "metadata": {
                    "system": {
                        "client": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
                        "ip_address": "108.168.19.134",
                        "location": "Kitchener, ON, Canada",
                        "latitude": 43.4103,
                        "longitude": -80.5038,
                    },
                    "custom": {},
                },
            },
            ZendeskSupportTicketCommentGet(
                author_id=114318908893,
                body="# H1\n\n## H2\n\n### H3\n\n#### H4\n\n##### H5\nNormal\n**Bold**\n**_BoldItalic_**\n_Italic_\n\n- Bullet1\n- Bullet2\n\n1. Number1\n2. Number2\n\n\nIndent\n\n\n\n> Quote\n\n\n`Code span`\n\n\n    Code block",
                created_at="2020-07-21T15:27:14Z",
                html_body='<div class="zd-comment" dir="auto"><h1 dir="auto">H1</h1><h2 dir="auto">H2</h2><h3 dir="auto">H3</h3><h4 dir="auto">H4</h4><h5 dir="auto">H5</h5>Normal<br><b>Bold</b><br><b><i>BoldItalic</i></b><br><i>Italic</i><br><ul dir="auto"><li>Bullet1</li><li>Bullet2</li></ul><ol dir="auto"><li>Number1</li><li>Number2</li></ol><br><div style="margin-left: 20px"><p dir="auto">Indent</p></div><br><blockquote><p dir="auto">Quote</p></blockquote><br><code>Code span</code><br><br><pre style="white-space: pre-wrap">Code block<br></pre><br></div>',
                id=1226851718033,
                public=True,
            ),
            None,
        ),
        (
            {
                "id": 1226596043794,
                "type": "Comment",
                "author_id": 365491090854,
                "body": "How can agents leverage knowledge to help customers?",
                "html_body": '<div class="zd-comment" dir="auto"><a href="https://d3v-meya.zendesk.com/hc/en-us/articles/360045161313-How-can-agents-leverage-knowledge-to-help-customers-?source=search&amp;auth_token=eyJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoxOTQ4NTAwLCJ1c2VyX2lkIjo0MTY0Nzc0OTQzNzMsInRpY2tldF9pZCI6MTUyOCwiY2hhbm5lbF9pZCI6NjMsInR5cGUiOiJTRUFSQ0giLCJleHAiOjE1OTc5Mzc1ODV9.RC5pyME-2lrCilemlTVoanAdgO8INhSKKAr1kTaUgr0" rel="noreferrer">How can agents leverage knowledge to help customers?</a><br></div>',
                "plain_body": "How can agents leverage knowledge to help customers?",
                "public": True,
                "attachments": [],
                "audit_id": 1226596043574,
                "via": {
                    "channel": "web",
                    "source": {"from": {}, "to": {}, "rel": None},
                },
                "created_at": "2020-07-21T15:33:29Z",
                "metadata": {
                    "system": {
                        "client": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
                        "ip_address": "108.168.19.134",
                        "location": "Kitchener, ON, Canada",
                        "latitude": 43.4103,
                        "longitude": -80.5038,
                    },
                    "custom": {},
                },
            },
            ZendeskSupportTicketCommentGet(
                author_id=365491090854,
                body="How can agents leverage knowledge to help customers?",
                created_at="2020-07-21T15:33:29Z",
                html_body='<div class="zd-comment" dir="auto"><a href="https://d3v-meya.zendesk.com/hc/en-us/articles/360045161313-How-can-agents-leverage-knowledge-to-help-customers-?source=search&amp;auth_token=eyJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoxOTQ4NTAwLCJ1c2VyX2lkIjo0MTY0Nzc0OTQzNzMsInRpY2tldF9pZCI6MTUyOCwiY2hhbm5lbF9pZCI6NjMsInR5cGUiOiJTRUFSQ0giLCJleHAiOjE1OTc5Mzc1ODV9.RC5pyME-2lrCilemlTVoanAdgO8INhSKKAr1kTaUgr0" rel="noreferrer">How can agents leverage knowledge to help customers?</a><br></div>',
                id=1226596043794,
                public=True,
            ),
            "[How can agents leverage knowledge to help customers?](https://d3v-meya.zendesk.com/hc/en-us/articles/360045161313-How-can-agents-leverage-knowledge-to-help-customers-?source=search&auth_token=eyJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50X2lkIjoxOTQ4NTAwLCJ1c2VyX2lkIjo0MTY0Nzc0OTQzNzMsInRpY2tldF9pZCI6MTUyOCwiY2hhbm5lbF9pZCI6NjMsInR5cGUiOiJTRUFSQ0giLCJleHAiOjE1OTc5Mzc1ODV9.RC5pyME-2lrCilemlTVoanAdgO8INhSKKAr1kTaUgr0)",
        ),
        (
            {
                "id": 1226885291873,
                "type": "Comment",
                "author_id": 114318908893,
                "body": "link abc, link def, link abc, link **ghi**",
                "html_body": '<div class="zd-comment" dir="auto"><a href="http://example.org/abc1" rel="noreferrer">link abc</a>, <a href="http://example.org/def" rel="noreferrer">link def</a>, <a href="http://example.org/abc2" rel="noreferrer">link abc</a>, <a href="http://example.org/ghi" rel="noreferrer">link <b>ghi</b></a><br></div>',
                "plain_body": "link abc, link def, link abc, link ghi",
                "public": True,
                "attachments": [],
                "audit_id": 1226885291733,
                "via": {
                    "channel": "web",
                    "source": {"from": {}, "to": {}, "rel": None},
                },
                "created_at": "2020-07-21T15:51:22Z",
                "metadata": {
                    "system": {
                        "client": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
                        "ip_address": "108.168.19.134",
                        "location": "Kitchener, ON, Canada",
                        "latitude": 43.4103,
                        "longitude": -80.5038,
                    },
                    "custom": {},
                },
            },
            ZendeskSupportTicketCommentGet(
                author_id=114318908893,
                body="link abc, link def, link abc, link **ghi**",
                html_body='<div class="zd-comment" dir="auto"><a href="http://example.org/abc1" rel="noreferrer">link abc</a>, <a href="http://example.org/def" rel="noreferrer">link def</a>, <a href="http://example.org/abc2" rel="noreferrer">link abc</a>, <a href="http://example.org/ghi" rel="noreferrer">link <b>ghi</b></a><br></div>',
                created_at="2020-07-21T15:51:22Z",
                id=1226885291873,
                public=True,
            ),
            "link abc, [link def](http://example.org/def), link abc, link **ghi**\n\nhttp://example.org/abc1\n\nhttp://example.org/abc2\n\nhttp://example.org/ghi",
        ),
        (
            {
                "id": 1226863125573,
                "type": "Comment",
                "author_id": 114318908893,
                "body": " ![](https://d3v-meya.zendesk.com/attachments/token/jP8qeWGM5JaK6DBYbSjBLwiEe/?name=inline811988885.png)\u200b",
                "html_body": '<div class="zd-comment" dir="auto"><img src="https://d3v-meya.zendesk.com/attachments/token/jP8qeWGM5JaK6DBYbSjBLwiEe/?name=inline811988885.png" data-original-height="172" data-original-width="292" style="height: auto; width: 292px">\u200b<br></div>',
                "plain_body": "\u200b",
                "public": True,
                "attachments": [],
                "audit_id": 1226863125193,
                "via": {
                    "channel": "web",
                    "source": {"from": {}, "to": {}, "rel": None},
                },
                "created_at": "2020-07-21T15:35:23Z",
                "metadata": {
                    "system": {
                        "client": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
                        "ip_address": "108.168.19.134",
                        "location": "Kitchener, ON, Canada",
                        "latitude": 43.4103,
                        "longitude": -80.5038,
                    },
                    "custom": {},
                },
            },
            ZendeskSupportTicketCommentGet(
                author_id=114318908893,
                body=" ![](https://d3v-meya.zendesk.com/attachments/token/jP8qeWGM5JaK6DBYbSjBLwiEe/?name=inline811988885.png)\u200b",
                public=True,
                created_at="2020-07-21T15:35:23Z",
                html_body='<div class="zd-comment" dir="auto"><img src="https://d3v-meya.zendesk.com/attachments/token/jP8qeWGM5JaK6DBYbSjBLwiEe/?name=inline811988885.png" data-original-height="172" data-original-width="292" style="height: auto; width: 292px">\u200b<br></div>',
                id=1226863125573,
            ),
            None,
        ),
        (
            {
                "id": 1226864834053,
                "type": "Comment",
                "author_id": 114318908893,
                "body": "Before\n\n* * *\nAfter",
                "html_body": '<div class="zd-comment" dir="auto">Before<br><hr>After<br></div>',
                "plain_body": "Before\n After",
                "public": True,
                "attachments": [],
                "audit_id": 1226864833873,
                "via": {
                    "channel": "web",
                    "source": {"from": {}, "to": {}, "rel": None},
                },
                "created_at": "2020-07-21T15:36:37Z",
                "metadata": {
                    "system": {
                        "client": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
                        "ip_address": "108.168.19.134",
                        "location": "Kitchener, ON, Canada",
                        "latitude": 43.4103,
                        "longitude": -80.5038,
                    },
                    "custom": {},
                },
            },
            ZendeskSupportTicketCommentGet(
                author_id=114318908893,
                body="Before\n\n* * *\nAfter",
                public=True,
                created_at="2020-07-21T15:36:37Z",
                html_body='<div class="zd-comment" dir="auto">Before<br><hr>After<br></div>',
                id=1226864834053,
            ),
            None,
        ),
    ],
)
def test_ticket_comment_get_from_dict(
    payload_dict: Dict[str, Any],
    payload: ZendeskSupportTicketCommentGet,
    body_with_links: Optional[str],
):
    assert ZendeskSupportTicketCommentGet.from_dict(payload_dict) == payload
    assert (body_with_links or payload.body) == payload.body_with_links
