from meya.front.payload.conversation import FrontConversationGet


def test_front_conversation_get():
    assert FrontConversationGet(
        id="cnv_b36e7yf", subject="", status="unassigned"
    ) == FrontConversationGet.from_dict(
        {
            "_links": {
                "self": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b36e7yf",
                "related": {
                    "events": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b36e7yf/events",
                    "followers": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b36e7yf/followers",
                    "messages": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b36e7yf/messages",
                    "comments": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b36e7yf/comments",
                    "inboxes": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b36e7yf/inboxes",
                },
            },
            "id": "cnv_b36e7yf",
            "subject": "",
            "status": "unassigned",
            "assignee": None,
            "recipient": {
                "_links": {"related": {"contact": None}},
                "handle": "meya_user/u-e715590655104210bfe6a19481aebeb5",
                "role": "from",
            },
            "tags": [],
            "last_message": {
                "_links": {
                    "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_og5cerr",
                    "related": {
                        "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b36e7yf"
                    },
                },
                "id": "msg_og5cerr",
                "type": "custom",
                "is_inbound": True,
                "created_at": 1623154758.542,
                "blurb": "(Conversation start)",
                "body": "<p>(Conversation start)</p>\n",
                "text": "(Conversation start)",
                "error_type": None,
                "version": None,
                "subject": "",
                "draft_mode": None,
                "metadata": {
                    "thread_ref": "meya_thread/t-80961d89f6354ef1969a4bdde4e5f72c"
                },
                "author": None,
                "recipients": [
                    {
                        "_links": {"related": {"contact": None}},
                        "handle": "meya_user/u-e715590655104210bfe6a19481aebeb5",
                        "role": "from",
                    },
                    {
                        "_links": {"related": {"contact": None}},
                        "handle": "e354054ec7334ed3",
                        "role": "to",
                    },
                ],
                "attachments": [],
                "is_draft": False,
            },
            "created_at": 1623154745.648,
            "is_private": False,
            "scheduled_reminders": [],
            "metadata": {},
        }
    )
