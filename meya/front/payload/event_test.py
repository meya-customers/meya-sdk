import pytest

from datetime import timedelta
from freezegun import freeze_time
from meya.element.element_test import frozen_milliseconds_timestamp
from meya.front.payload.comment import FrontCommentGet
from meya.front.payload.conversation import FrontConversationGet
from meya.front.payload.event import FrontActionEvent
from meya.front.payload.event import FrontAssignEvent
from meya.front.payload.event import FrontChannelMessageEvent
from meya.front.payload.event import FrontCommentEvent
from meya.front.payload.event import FrontCustomMessageEvent
from meya.front.payload.event import FrontEvent
from meya.front.payload.event import FrontEventCommentData
from meya.front.payload.event import FrontEventMessageData
from meya.front.payload.event import FrontInboundEvent
from meya.front.payload.event import FrontOutboundEvent
from meya.front.payload.event import FrontReopenConversationEvent
from meya.front.payload.event import FrontRestoreConversationEvent
from meya.front.payload.event import FrontSourceTargetData
from meya.front.payload.event import FrontSourceTargetMeta
from meya.front.payload.event import FrontSourceTargetMetaType
from meya.front.payload.event import FrontTagEvent
from meya.front.payload.event import FrontTrashConversationEvent
from meya.front.payload.event import FrontUnassignEvent
from meya.front.payload.event import FrontUntagEvent
from meya.front.payload.message import FrontCustomChannelHeaders
from meya.front.payload.message import FrontCustomChannelMetadata
from meya.front.payload.message import FrontMessageGet
from meya.front.payload.message import FrontMessageGetMetadata
from meya.front.payload.message import FrontMessageGetRecipient
from meya.front.payload.message import FrontMessageGetRecipientLinks
from meya.front.payload.message import FrontMessageGetRecipientRelated
from meya.front.payload.message import FrontPartnerChannelMessage
from meya.front.payload.message import FrontPartnerChannelMetadata
from meya.front.payload.rules import FrontRule
from meya.front.payload.tag import FrontTagTarget
from meya.front.payload.tag import FrontTagTargetData
from meya.front.payload.teammate import FrontTeammateGet
from meya.time.time import from_utc_milliseconds_timestamp
from unittest.mock import MagicMock


def test_front_message_event_from_dict():
    assert FrontEvent.from_typed_dict(
        {
            "id": "msg_hihs0qv",
            "body": "Hi there, welcome to Meya",
            "text": "Hi there, welcome to Meya",
            "type": "custom",
            "blurb": "Hi there, welcome to Meya",
            "_links": {
                "self": "https://api2.frontapp.com/messages/msg_hihs0qv",
                "related": {
                    "conversation": "https://api2.frontapp.com/conversations/cnv_8oyif9j",
                    "message_replied_to": "https://api2.frontapp.com/messages/msg_hihs0qv/parent",
                },
            },
            "author": {
                "id": "tea_b2c7",
                "email": "amanie@meya.ai",
                "_links": {
                    "self": "https://api2.frontapp.com/teammates/tea_b2c7",
                    "related": {
                        "inboxes": "https://api2.frontapp.com/teammates/tea_b2c7/inboxes",
                        "conversations": "https://api2.frontapp.com/teammates/tea_b2c7/conversations",
                    },
                },
                "is_admin": True,
                "username": "amanie",
                "last_name": "Ismail",
                "first_name": "Amanie",
                "is_blocked": False,
                "is_available": True,
            },
            "subject": "Re: ",
            "version": "6e4b054926f829a8720cd56d911b7631-318607-1602100742100-a010",
            "is_draft": True,
            "metadata": {
                "headers": {
                    "in_reply_to": "imported@frontapp.com_8b717e98222977443321401cd6536370d9193071"
                }
            },
            "created_at": 1602100742.249,
            "error_type": "webhook_error",
            "is_inbound": False,
            "recipients": [
                {
                    "role": "from",
                    "_links": {"related": {"contact": None}},
                    "handle": "ba490680fd1da827",
                },
                {
                    "role": "to",
                    "_links": {"related": {"contact": None}},
                    "handle": "u8",
                },
            ],
            "attachments": [],
        }
    ) == FrontCustomMessageEvent(
        id="msg_hihs0qv",
        is_inbound=False,
        body="Hi there, welcome to Meya",
        links=FrontMessageGetRecipientLinks(
            related=FrontMessageGetRecipientRelated(
                conversation="https://api2.frontapp.com/conversations/cnv_8oyif9j"
            )
        ),
        author=FrontTeammateGet(
            id="tea_b2c7",
            email="amanie@meya.ai",
            first_name="Amanie",
            last_name="Ismail",
            username="amanie",
            is_admin=True,
            is_available=True,
            is_blocked=False,
        ),
        created_at=1602100742.249,
        recipients=[
            FrontMessageGetRecipient(
                role="from",
                links=FrontMessageGetRecipientLinks(
                    related=FrontMessageGetRecipientRelated(contact=None)
                ),
                handle="ba490680fd1da827",
            ),
            FrontMessageGetRecipient(
                role="to",
                links=FrontMessageGetRecipientLinks(
                    related=FrontMessageGetRecipientRelated(contact=None)
                ),
                handle="u8",
            ),
        ],
        text="Hi there, welcome to Meya",
        type="custom",
        metadata=FrontCustomChannelMetadata(
            headers=FrontCustomChannelHeaders(
                in_reply_to="imported@frontapp.com_8b717e98222977443321401cd6536370d9193071"
            ),
        ),
    )


def test_front_inbound_event_from_dict():
    assert FrontEvent.from_typed_dict(
        {
            "id": "evt_170nwumf",
            "type": "inbound",
            "_links": {
                "self": "https://api2.frontapp.com/events/evt_170nwumf"
            },
            "source": {
                "data": [
                    {
                        "id": "inb_326dj",
                        "name": "Front + Meya [test]",
                        "type": "custom",
                        "_links": {
                            "self": "https://api2.frontapp.com/inboxes/inb_326dj",
                            "related": {
                                "owner": "https://api2.frontapp.com/teams/tim_6xuv",
                                "channels": "https://api2.frontapp.com/inboxes/inb_326dj/channels",
                                "teammates": "https://api2.frontapp.com/inboxes/inb_326dj/teammates",
                                "conversations": "https://api2.frontapp.com/inboxes/inb_326dj/conversations",
                            },
                        },
                        "address": "513656ca54a75bf0",
                        "send_as": "513656ca54a75bf0",
                        "is_public": False,
                        "is_private": False,
                    }
                ],
                "_meta": {"type": "inboxes"},
            },
            "target": {
                "data": {
                    "id": "msg_huqqdjb",
                    "body": "<p>(Conversation start)</p>\n",
                    "text": "(Conversation start)",
                    "type": "custom",
                    "blurb": "(Conversation start)",
                    "_links": {
                        "self": "https://api2.frontapp.com/messages/msg_huqqdjb",
                        "related": {
                            "conversation": "https://api2.frontapp.com/conversations/cnv_8t0yivb"
                        },
                    },
                    "author": None,
                    "subject": "Meya conversation",
                    "version": None,
                    "is_draft": False,
                    "metadata": {
                        "thread_ref": "meya_thread/t-c05dce56d9234d2b989473101c88f9db"
                    },
                    "created_at": 1603216662.672,
                    "error_type": None,
                    "is_inbound": True,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {
                                "related": {
                                    "contact": "https://api2.frontapp.com/contacts/crd_10wxxqf"
                                }
                            },
                            "handle": "meya_user/u-5ec50afb51e246689f89cfb0cd4ab065",
                        },
                        {
                            "role": "to",
                            "_links": {"related": {"contact": None}},
                            "handle": "513656ca54a75bf0",
                        },
                    ],
                    "attachments": [],
                },
                "_meta": {"type": "message"},
            },
            "emitted_at": 1603216662.672,
            "conversation": {
                "id": "cnv_8t0yivb",
                "tags": [],
                "_links": {
                    "self": "https://api2.frontapp.com/conversations/cnv_8t0yivb",
                    "related": {
                        "events": "https://api2.frontapp.com/conversations/cnv_8t0yivb/events",
                        "inboxes": "https://api2.frontapp.com/conversations/cnv_8t0yivb/inboxes",
                        "comments": "https://api2.frontapp.com/conversations/cnv_8t0yivb/comments",
                        "messages": "https://api2.frontapp.com/conversations/cnv_8t0yivb/messages",
                        "followers": "https://api2.frontapp.com/conversations/cnv_8t0yivb/followers",
                    },
                },
                "status": "unassigned",
                "subject": "Meya conversation",
                "assignee": None,
                "recipient": {
                    "role": "from",
                    "_links": {"related": {"contact": None}},
                    "handle": "meya_user/u-5ec50afb51e246689f89cfb0cd4ab065",
                },
                "created_at": 1603216662.926,
                "is_private": False,
                "last_message": {
                    "id": "msg_huqqdjb",
                    "body": "<p>(Conversation start)</p>\n",
                    "text": "(Conversation start)",
                    "type": "custom",
                    "blurb": "(Conversation start)",
                    "_links": {
                        "self": "https://api2.frontapp.com/messages/msg_huqqdjb",
                        "related": {
                            "conversation": "https://api2.frontapp.com/conversations/cnv_8t0yivb"
                        },
                    },
                    "author": None,
                    "subject": "Meya conversation",
                    "version": None,
                    "is_draft": False,
                    "metadata": {
                        "thread_ref": "meya_thread/t-c05dce56d9234d2b989473101c88f9db"
                    },
                    "created_at": 1603216662.672,
                    "error_type": None,
                    "is_inbound": True,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {"related": {"contact": None}},
                            "handle": "meya_user/u-5ec50afb51e246689f89cfb0cd4ab065",
                        },
                        {
                            "role": "to",
                            "_links": {"related": {"contact": None}},
                            "handle": "513656ca54a75bf0",
                        },
                    ],
                    "attachments": [],
                },
            },
        }
    ) == FrontInboundEvent(
        conversation=FrontConversationGet(
            status="unassigned", id="cnv_8t0yivb", subject="Meya conversation"
        ),
        emitted_at=1603216662.672,
        target=FrontEventMessageData(
            data=FrontMessageGet(
                body="<p>(Conversation start)</p>\n",
                created_at=1603216662.672,
                metadata=FrontMessageGetMetadata(
                    thread_ref="meya_thread/t-c05dce56d9234d2b989473101c88f9db"
                ),
                recipients=[
                    FrontMessageGetRecipient(
                        links=FrontMessageGetRecipientLinks(
                            related=FrontMessageGetRecipientRelated(
                                contact="https://api2.frontapp.com/contacts/crd_10wxxqf"
                            )
                        ),
                        handle="meya_user/u-5ec50afb51e246689f89cfb0cd4ab065",
                        role="from",
                    ),
                    FrontMessageGetRecipient(
                        handle="513656ca54a75bf0", role="to"
                    ),
                ],
                text="(Conversation start)",
                type="custom",
            )
        ),
    )


@pytest.mark.parametrize(
    ("payload", "obj"),
    [
        (
            {
                "id": "evt_168fw2vb",
                "type": "outbound",
                "_links": {
                    "self": "https://api2.frontapp.com/events/evt_168fw2vb"
                },
                "source": {
                    "data": [
                        {
                            "id": "inb_326dj",
                            "name": "demo-app [dc]",
                            "type": "custom",
                            "_links": {
                                "self": "https://api2.frontapp.com/inboxes/inb_326dj",
                                "related": {
                                    "owner": "https://api2.frontapp.com/teams/tim_6xuv",
                                    "channels": "https://api2.frontapp.com/inboxes/inb_326dj/channels",
                                    "teammates": "https://api2.frontapp.com/inboxes/inb_326dj/teammates",
                                    "conversations": "https://api2.frontapp.com/inboxes/inb_326dj/conversations",
                                },
                            },
                            "address": "513656ca54a75bf0",
                            "send_as": "513656ca54a75bf0",
                            "is_private": False,
                        }
                    ],
                    "_meta": {"type": "inboxes"},
                },
                "target": {
                    "data": {
                        "id": "msg_hisjtdz",
                        "body": "Hey there",
                        "text": "Hey there",
                        "type": "custom",
                        "blurb": "Hey there",
                        "_links": {
                            "self": "https://api2.frontapp.com/messages/msg_hisjtdz",
                            "related": {
                                "conversation": "https://api2.frontapp.com/conversations/cnv_8p2i0w7",
                                "message_replied_to": "https://api2.frontapp.com/messages/msg_hisjtdz/parent",
                            },
                        },
                        "author": {
                            "id": "tea_b2c7",
                            "email": "amanie@meya.ai",
                            "_links": {
                                "self": "https://api2.frontapp.com/teammates/tea_b2c7",
                                "related": {
                                    "inboxes": "https://api2.frontapp.com/teammates/tea_b2c7/inboxes",
                                    "conversations": "https://api2.frontapp.com/teammates/tea_b2c7/conversations",
                                },
                            },
                            "is_admin": True,
                            "username": "amanie",
                            "last_name": "Ismail",
                            "first_name": "Amanie",
                            "is_blocked": False,
                            "is_available": True,
                        },
                        "subject": "Re: ",
                        "version": None,
                        "is_draft": False,
                        "metadata": {
                            "headers": {
                                "in_reply_to": "imported@frontapp.com_fd872a0ba3a60e30668624c2729a0d4b4a99612a"
                            }
                        },
                        "created_at": 1602124711.073,
                        "error_type": None,
                        "is_inbound": False,
                        "recipients": [
                            {
                                "role": "from",
                                "_links": {"related": {"contact": None}},
                                "handle": "513656ca54a75bf0",
                            },
                            {
                                "role": "to",
                                "_links": {
                                    "related": {
                                        "contact": "https://api2.frontapp.com/contacts/crd_10gex6v"
                                    }
                                },
                                "handle": "u-7a23ddb597cb435ebbf60ec1ad311a13",
                            },
                        ],
                        "attachments": [],
                    },
                    "_meta": {"type": "message"},
                },
                "emitted_at": 1602124711.073,
                "conversation": {
                    "id": "cnv_8p2i0w7",
                    "tags": [],
                    "_links": {
                        "self": "https://api2.frontapp.com/conversations/cnv_8p2i0w7",
                        "related": {
                            "events": "https://api2.frontapp.com/conversations/cnv_8p2i0w7/events",
                            "inboxes": "https://api2.frontapp.com/conversations/cnv_8p2i0w7/inboxes",
                            "comments": "https://api2.frontapp.com/conversations/cnv_8p2i0w7/comments",
                            "messages": "https://api2.frontapp.com/conversations/cnv_8p2i0w7/messages",
                            "followers": "https://api2.frontapp.com/conversations/cnv_8p2i0w7/followers",
                        },
                    },
                    "status": "archived",
                    "subject": "Re: ",
                    "assignee": {
                        "id": "tea_b2c7",
                        "email": "amanie@meya.ai",
                        "_links": {
                            "self": "https://api2.frontapp.com/teammates/tea_b2c7",
                            "related": {
                                "inboxes": "https://api2.frontapp.com/teammates/tea_b2c7/inboxes",
                                "conversations": "https://api2.frontapp.com/teammates/tea_b2c7/conversations",
                            },
                        },
                        "is_admin": True,
                        "username": "amanie",
                        "last_name": "Ismail",
                        "first_name": "Amanie",
                        "is_blocked": False,
                        "is_available": True,
                    },
                    "recipient": {
                        "role": "to",
                        "_links": {
                            "related": {
                                "contact": "https://api2.frontapp.com/contacts/crd_10gex6v"
                            }
                        },
                        "handle": "u-7a23ddb597cb435ebbf60ec1ad311a13",
                    },
                    "created_at": 1602121695.901,
                    "is_private": False,
                    "last_message": {
                        "id": "msg_hisjtdz",
                        "body": "Hey there",
                        "text": "Hey there",
                        "type": "custom",
                        "blurb": "Hey there",
                        "_links": {
                            "self": "https://api2.frontapp.com/messages/msg_hisjtdz",
                            "related": {
                                "conversation": "https://api2.frontapp.com/conversations/cnv_8p2i0w7",
                                "message_replied_to": "https://api2.frontapp.com/messages/msg_hisjtdz/parent",
                            },
                        },
                        "author": {
                            "id": "tea_b2c7",
                            "email": "amanie@meya.ai",
                            "_links": {
                                "self": "https://api2.frontapp.com/teammates/tea_b2c7",
                                "related": {
                                    "inboxes": "https://api2.frontapp.com/teammates/tea_b2c7/inboxes",
                                    "conversations": "https://api2.frontapp.com/teammates/tea_b2c7/conversations",
                                },
                            },
                            "is_admin": True,
                            "username": "amanie",
                            "last_name": "Ismail",
                            "first_name": "Amanie",
                            "is_blocked": False,
                            "is_available": True,
                        },
                        "subject": "Re: ",
                        "version": None,
                        "is_draft": False,
                        "metadata": {
                            "headers": {
                                "in_reply_to": "imported@frontapp.com_fd872a0ba3a60e30668624c2729a0d4b4a99612a"
                            }
                        },
                        "created_at": 1602124711.073,
                        "error_type": None,
                        "is_inbound": False,
                        "recipients": [
                            {
                                "role": "from",
                                "_links": {"related": {"contact": None}},
                                "handle": "513656ca54a75bf0",
                            },
                            {
                                "role": "to",
                                "_links": {
                                    "related": {
                                        "contact": "https://api2.frontapp.com/contacts/crd_10gex6v"
                                    }
                                },
                                "handle": "u-7a23ddb597cb435ebbf60ec1ad311a13",
                            },
                        ],
                        "attachments": [],
                    },
                },
            },
            FrontOutboundEvent(
                conversation=FrontConversationGet(
                    status="archived",
                    id="cnv_8p2i0w7",
                    subject="Re: ",
                    assignee=FrontTeammateGet(
                        id="tea_b2c7",
                        first_name="Amanie",
                        last_name="Ismail",
                        email="amanie@meya.ai",
                        username="amanie",
                        is_admin=True,
                        is_available=True,
                        is_blocked=False,
                    ),
                ),
                emitted_at=1602124711.073,
                target=FrontEventMessageData(
                    data=FrontMessageGet(
                        body="Hey there",
                        author=FrontTeammateGet(
                            email="amanie@meya.ai",
                            first_name="Amanie",
                            last_name="Ismail",
                            id="tea_b2c7",
                            username="amanie",
                            is_admin=True,
                            is_available=True,
                            is_blocked=False,
                        ),
                        created_at=1602124711.073,
                        recipients=[
                            FrontMessageGetRecipient(
                                handle="513656ca54a75bf0", role="from"
                            ),
                            FrontMessageGetRecipient(
                                links=FrontMessageGetRecipientLinks(
                                    related=FrontMessageGetRecipientRelated(
                                        contact="https://api2.frontapp.com/contacts/crd_10gex6v"
                                    )
                                ),
                                handle="u-7a23ddb597cb435ebbf60ec1ad311a13",
                                role="to",
                            ),
                        ],
                        text="Hey there",
                        type="custom",
                    )
                ),
            ),
        ),
        (
            {
                "id": "evt_1vbxwf2f",
                "type": "outbound",
                "_links": {
                    "self": "https://meya-partner-developer-account.api.frontapp.com/events/evt_1vbxwf2f"
                },
                "source": {
                    "data": [
                        {
                            "id": "inb_3d3t3",
                            "name": "demo-app [joao]",
                            "type": "custom",
                            "_links": {
                                "self": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d3t3",
                                "related": {
                                    "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                                    "channels": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d3t3/channels",
                                    "teammates": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d3t3/teammates",
                                    "conversations": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d3t3/conversations",
                                },
                            },
                            "address": "e354054ec7334ed3",
                            "send_as": "e354054ec7334ed3",
                            "is_public": False,
                            "is_private": False,
                            "custom_fields": {},
                        }
                    ],
                    "_meta": {"type": "inboxes"},
                },
                "target": {
                    "data": {
                        "id": "msg_scojk07",
                        "body": "Hey",
                        "text": "Hey",
                        "type": "custom",
                        "blurb": "Hey",
                        "_links": {
                            "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_scojk07",
                            "related": {
                                "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_cdxi007"
                            },
                        },
                        "author": {
                            "id": "tea_b2c7",
                            "email": "amanie@meya.ai",
                            "_links": {
                                "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                                "related": {
                                    "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                                    "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                                },
                            },
                            "is_admin": True,
                            "username": "amanie",
                            "last_name": "Ismail",
                            "first_name": "Amanie",
                            "is_blocked": False,
                            "is_available": True,
                            "custom_fields": {},
                        },
                        "subject": "",
                        "version": None,
                        "is_draft": False,
                        "metadata": {"headers": {"in_reply_to": None}},
                        "created_at": 1633528611.31,
                        "draft_mode": None,
                        "error_type": None,
                        "is_inbound": False,
                        "recipients": [
                            {
                                "role": "from",
                                "_links": {"related": {"contact": None}},
                                "handle": "e354054ec7334ed3",
                            },
                            {
                                "role": "to",
                                "_links": {
                                    "related": {
                                        "contact": "https://api2.frontapp.com/contacts/crd_1q51213"
                                    }
                                },
                                "handle": "joao@meya.ai",
                            },
                        ],
                        "attachments": [],
                    },
                    "_meta": {"type": "message"},
                },
                "emitted_at": 1633528611.31,
                "conversation": {
                    "id": "cnv_cdxi007",
                    "tags": [],
                    "links": [],
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_cdxi007",
                        "related": {
                            "events": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_cdxi007/events",
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_cdxi007/inboxes",
                            "comments": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_cdxi007/comments",
                            "messages": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_cdxi007/messages",
                            "followers": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_cdxi007/followers",
                        },
                    },
                    "status": "assigned",
                    "topics": [],
                    "subject": "",
                    "assignee": {
                        "id": "tea_b2c7",
                        "email": "amanie@meya.ai",
                        "_links": {
                            "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                            "related": {
                                "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                                "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                            },
                        },
                        "is_admin": True,
                        "username": "amanie",
                        "last_name": "Ismail",
                        "first_name": "Amanie",
                        "is_blocked": False,
                        "is_available": True,
                        "custom_fields": {},
                    },
                    "metadata": {},
                    "recipient": {
                        "role": "to",
                        "_links": {
                            "related": {
                                "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1q51213"
                            }
                        },
                        "handle": "joao@meya.ai",
                    },
                    "created_at": 1633528605.92,
                    "is_private": False,
                    "last_message": {
                        "id": "msg_scojk07",
                        "body": "Hey",
                        "text": "Hey",
                        "type": "custom",
                        "blurb": "Hey",
                        "_links": {
                            "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_scojk07",
                            "related": {
                                "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_cdxi007"
                            },
                        },
                        "author": {
                            "id": "tea_b2c7",
                            "email": "amanie@meya.ai",
                            "_links": {
                                "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                                "related": {
                                    "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                                    "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                                },
                            },
                            "is_admin": True,
                            "username": "amanie",
                            "last_name": "Ismail",
                            "first_name": "Amanie",
                            "is_blocked": False,
                            "is_available": True,
                            "custom_fields": {},
                        },
                        "subject": "",
                        "version": None,
                        "is_draft": False,
                        "metadata": {"headers": {"in_reply_to": None}},
                        "created_at": 1633528611.31,
                        "draft_mode": None,
                        "error_type": None,
                        "is_inbound": False,
                        "recipients": [
                            {
                                "role": "from",
                                "_links": {"related": {"contact": None}},
                                "handle": "e354054ec7334ed3",
                            },
                            {
                                "role": "to",
                                "_links": {
                                    "related": {
                                        "contact": "https://api2.frontapp.com/contacts/crd_1q51213"
                                    }
                                },
                                "handle": "joao@meya.ai",
                            },
                        ],
                        "attachments": [],
                    },
                    "scheduled_reminders": [],
                },
            },
            FrontOutboundEvent(
                conversation=FrontConversationGet(
                    status="assigned",
                    id="cnv_cdxi007",
                    subject="",
                    assignee=FrontTeammateGet(
                        id="tea_b2c7",
                        first_name="Amanie",
                        last_name="Ismail",
                        email="amanie@meya.ai",
                        username="amanie",
                        is_admin=True,
                        is_available=True,
                        is_blocked=False,
                    ),
                ),
                emitted_at=1633528611.31,
                target=FrontEventMessageData(
                    data=FrontMessageGet(
                        body="Hey",
                        author=FrontTeammateGet(
                            email="amanie@meya.ai",
                            first_name="Amanie",
                            last_name="Ismail",
                            id="tea_b2c7",
                            username="amanie",
                            is_admin=True,
                            is_available=True,
                            is_blocked=False,
                        ),
                        created_at=1633528611.31,
                        recipients=[
                            FrontMessageGetRecipient(
                                handle="e354054ec7334ed3", role="from"
                            ),
                            FrontMessageGetRecipient(
                                links=FrontMessageGetRecipientLinks(
                                    related=FrontMessageGetRecipientRelated(
                                        contact="https://api2.frontapp.com/contacts/crd_1q51213"
                                    )
                                ),
                                handle="joao@meya.ai",
                                role="to",
                            ),
                        ],
                        text="Hey",
                        type="custom",
                    )
                ),
            ),
        ),
    ],
)
def test_front_outbound_event_from_dict(payload, obj):
    assert FrontEvent.from_typed_dict(payload) == obj


def test_front_out_reply_event_from_dict():
    assert FrontEvent.from_typed_dict(
        {
            "id": "evt_168gzxl3",
            "type": "out_reply",
            "_links": {
                "self": "https://api2.frontapp.com/events/evt_168gzxl3"
            },
            "source": {
                "data": [
                    {
                        "id": "inb_326dj",
                        "name": "demo-app [dc]",
                        "type": "custom",
                        "_links": {
                            "self": "https://api2.frontapp.com/inboxes/inb_326dj",
                            "related": {
                                "owner": "https://api2.frontapp.com/teams/tim_6xuv",
                                "channels": "https://api2.frontapp.com/inboxes/inb_326dj/channels",
                                "teammates": "https://api2.frontapp.com/inboxes/inb_326dj/teammates",
                                "conversations": "https://api2.frontapp.com/inboxes/inb_326dj/conversations",
                            },
                        },
                        "address": "513656ca54a75bf0",
                        "send_as": "513656ca54a75bf0",
                        "is_private": False,
                    }
                ],
                "_meta": {"type": "inboxes"},
            },
            "target": {
                "data": {
                    "id": "msg_hit0og7",
                    "body": "Hold on there",
                    "text": "Hold on there",
                    "type": "custom",
                    "blurb": "Hold on there",
                    "_links": {
                        "self": "https://api2.frontapp.com/messages/msg_hit0og7",
                        "related": {
                            "conversation": "https://api2.frontapp.com/conversations/cnv_8p2zm4n",
                            "message_replied_to": "https://api2.frontapp.com/messages/msg_hit0og7/parent",
                        },
                    },
                    "author": {
                        "id": "tea_b2c7",
                        "email": "amanie@meya.ai",
                        "_links": {
                            "self": "https://api2.frontapp.com/teammates/tea_b2c7",
                            "related": {
                                "inboxes": "https://api2.frontapp.com/teammates/tea_b2c7/inboxes",
                                "conversations": "https://api2.frontapp.com/teammates/tea_b2c7/conversations",
                            },
                        },
                        "is_admin": True,
                        "username": "amanie",
                        "last_name": "Ismail",
                        "first_name": "Amanie",
                        "is_blocked": False,
                        "is_available": True,
                    },
                    "subject": "Re: ",
                    "version": None,
                    "is_draft": False,
                    "metadata": {
                        "headers": {
                            "in_reply_to": "imported@frontapp.com_f0e6c4c75716ab7c326c047e161abc0b5bc46eb9"
                        }
                    },
                    "created_at": 1602126660.31,
                    "error_type": None,
                    "is_inbound": False,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {"related": {"contact": None}},
                            "handle": "513656ca54a75bf0",
                        },
                        {
                            "role": "to",
                            "_links": {
                                "related": {
                                    "contact": "https://api2.frontapp.com/contacts/crd_10gj07b"
                                }
                            },
                            "handle": "meya_user/u-7a23ddb597cb435ebbf60ec1ad311a13",
                        },
                    ],
                    "attachments": [],
                },
                "_meta": {"type": "message"},
            },
            "emitted_at": 1602126660.31,
            "conversation": {
                "id": "cnv_8p2zm4n",
                "tags": [],
                "_links": {
                    "self": "https://api2.frontapp.com/conversations/cnv_8p2zm4n",
                    "related": {
                        "events": "https://api2.frontapp.com/conversations/cnv_8p2zm4n/events",
                        "inboxes": "https://api2.frontapp.com/conversations/cnv_8p2zm4n/inboxes",
                        "comments": "https://api2.frontapp.com/conversations/cnv_8p2zm4n/comments",
                        "messages": "https://api2.frontapp.com/conversations/cnv_8p2zm4n/messages",
                        "followers": "https://api2.frontapp.com/conversations/cnv_8p2zm4n/followers",
                    },
                },
                "status": "archived",
                "subject": "Re: ",
                "assignee": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://api2.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://api2.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://api2.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                },
                "recipient": {
                    "role": "to",
                    "_links": {
                        "related": {
                            "contact": "https://api2.frontapp.com/contacts/crd_10gj07b"
                        }
                    },
                    "handle": "meya_user/u-7a23ddb597cb435ebbf60ec1ad311a13",
                },
                "created_at": 1602126548.545,
                "is_private": False,
                "last_message": {
                    "id": "msg_hit0og7",
                    "body": "Hold on there",
                    "text": "Hold on there",
                    "type": "custom",
                    "blurb": "Hold on there",
                    "_links": {
                        "self": "https://api2.frontapp.com/messages/msg_hit0og7",
                        "related": {
                            "conversation": "https://api2.frontapp.com/conversations/cnv_8p2zm4n",
                            "message_replied_to": "https://api2.frontapp.com/messages/msg_hit0og7/parent",
                        },
                    },
                    "author": {
                        "id": "tea_b2c7",
                        "email": "amanie@meya.ai",
                        "_links": {
                            "self": "https://api2.frontapp.com/teammates/tea_b2c7",
                            "related": {
                                "inboxes": "https://api2.frontapp.com/teammates/tea_b2c7/inboxes",
                                "conversations": "https://api2.frontapp.com/teammates/tea_b2c7/conversations",
                            },
                        },
                        "is_admin": True,
                        "username": "amanie",
                        "last_name": "Ismail",
                        "first_name": "Amanie",
                        "is_blocked": False,
                        "is_available": True,
                    },
                    "subject": "Re: ",
                    "version": None,
                    "is_draft": False,
                    "metadata": {
                        "headers": {
                            "in_reply_to": "imported@frontapp.com_f0e6c4c75716ab7c326c047e161abc0b5bc46eb9"
                        }
                    },
                    "created_at": 1602126660.31,
                    "error_type": None,
                    "is_inbound": False,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {"related": {"contact": None}},
                            "handle": "513656ca54a75bf0",
                        },
                        {
                            "role": "to",
                            "_links": {
                                "related": {
                                    "contact": "https://api2.frontapp.com/contacts/crd_10gj07b"
                                }
                            },
                            "handle": "meya_user/u-7a23ddb597cb435ebbf60ec1ad311a13",
                        },
                    ],
                    "attachments": [],
                },
            },
        }
    ) == FrontOutboundEvent(
        conversation=FrontConversationGet(
            status="archived",
            id="cnv_8p2zm4n",
            subject="Re: ",
            assignee=FrontTeammateGet(
                id="tea_b2c7",
                first_name="Amanie",
                last_name="Ismail",
                email="amanie@meya.ai",
                username="amanie",
                is_admin=True,
                is_available=True,
                is_blocked=False,
                custom_fields={},
            ),
        ),
        emitted_at=1602126660.31,
        target=FrontEventMessageData(
            data=FrontMessageGet(
                body="Hold on there",
                author=FrontTeammateGet(
                    email="amanie@meya.ai",
                    first_name="Amanie",
                    id="tea_b2c7",
                    last_name="Ismail",
                    username="amanie",
                    is_admin=True,
                    is_available=True,
                    is_blocked=False,
                ),
                created_at=1602126660.31,
                recipients=[
                    FrontMessageGetRecipient(
                        handle="513656ca54a75bf0", role="from"
                    ),
                    FrontMessageGetRecipient(
                        links=FrontMessageGetRecipientLinks(
                            related=FrontMessageGetRecipientRelated(
                                contact="https://api2.frontapp.com/contacts/crd_10gj07b"
                            )
                        ),
                        handle="meya_user/u-7a23ddb597cb435ebbf60ec1ad311a13",
                        role="to",
                    ),
                ],
                text="Hold on there",
                type="custom",
            )
        ),
    )


def test_front_assign_event_from_dict():
    assert FrontEvent.from_typed_dict(
        {
            "id": "evt_170tvufb",
            "type": "assign",
            "_links": {
                "self": "https://api2.frontapp.com/events/evt_170tvufb"
            },
            "source": {
                "data": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://api2.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://api2.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://api2.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                },
                "_meta": {"type": "teammate"},
            },
            "target": {
                "data": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://api2.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://api2.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://api2.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                },
                "_meta": {"type": "teammate"},
            },
            "emitted_at": 1603219092.531,
            "conversation": {
                "id": "cnv_8t1qgef",
                "tags": [],
                "_links": {
                    "self": "https://api2.frontapp.com/conversations/cnv_8t1qgef",
                    "related": {
                        "events": "https://api2.frontapp.com/conversations/cnv_8t1qgef/events",
                        "inboxes": "https://api2.frontapp.com/conversations/cnv_8t1qgef/inboxes",
                        "comments": "https://api2.frontapp.com/conversations/cnv_8t1qgef/comments",
                        "messages": "https://api2.frontapp.com/conversations/cnv_8t1qgef/messages",
                        "followers": "https://api2.frontapp.com/conversations/cnv_8t1qgef/followers",
                    },
                },
                "status": "assigned",
                "subject": "Re: Meya conversation",
                "assignee": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://api2.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://api2.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://api2.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                },
                "recipient": {
                    "role": "to",
                    "_links": {
                        "related": {
                            "contact": "https://api2.frontapp.com/contacts/crd_10vcih3"
                        }
                    },
                    "handle": "meya_user/u-29ec8a82e87544fb9e4e35dc620fb5d1",
                },
                "created_at": 1603218811.244,
                "is_private": False,
                "last_message": {
                    "id": "msg_hutb30n",
                    "body": "Sorry, I don't understand.\n--&gt; [email]\n--&gt; [random]\n--&gt; [catchall]",
                    "text": "Sorry, I don't understand.\n--> [email]\n--> [random]\n--> [catchall]",
                    "type": "custom",
                    "blurb": "",
                    "_links": {
                        "self": "https://api2.frontapp.com/messages/msg_hutb30n",
                        "related": {
                            "conversation": "https://api2.frontapp.com/conversations/cnv_8t1qgef",
                            "message_replied_to": "https://api2.frontapp.com/messages/msg_hutb30n/parent",
                        },
                    },
                    "author": {
                        "id": "tea_d0tj",
                        "email": "support@meya.ai",
                        "_links": {
                            "self": "https://api2.frontapp.com/teammates/tea_d0tj",
                            "related": {
                                "inboxes": "https://api2.frontapp.com/teammates/tea_d0tj/inboxes",
                                "conversations": "https://api2.frontapp.com/teammates/tea_d0tj/conversations",
                            },
                        },
                        "is_admin": True,
                        "username": "support",
                        "last_name": "Bot",
                        "first_name": "Meya",
                        "is_blocked": False,
                        "is_available": True,
                    },
                    "subject": "Re: Meya conversation",
                    "version": None,
                    "is_draft": False,
                    "metadata": {
                        "headers": {"in_reply_to": "b48bb9897b76710d"}
                    },
                    "created_at": 1603218890.934,
                    "error_type": None,
                    "is_inbound": False,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {"related": {"contact": None}},
                            "handle": "513656ca54a75bf0",
                        },
                        {
                            "role": "to",
                            "_links": {
                                "related": {
                                    "contact": "https://api2.frontapp.com/contacts/crd_10vcih3"
                                }
                            },
                            "handle": "meya_user/u-29ec8a82e87544fb9e4e35dc620fb5d1",
                        },
                    ],
                    "attachments": [],
                },
            },
        }
    ) == FrontAssignEvent(
        conversation=FrontConversationGet(
            id="cnv_8t1qgef",
            status="assigned",
            subject="Re: Meya conversation",
            assignee=FrontTeammateGet(
                id="tea_b2c7",
                email="amanie@meya.ai",
                first_name="Amanie",
                last_name="Ismail",
                username="amanie",
                is_admin=True,
                is_available=True,
                is_blocked=False,
            ),
        ),
        emitted_at=1603219092.531,
        target=FrontSourceTargetData(
            data=FrontTeammateGet(
                email="amanie@meya.ai",
                first_name="Amanie",
                id="tea_b2c7",
                last_name="Ismail",
                username="amanie",
                is_admin=True,
                is_available=True,
                is_blocked=False,
            ),
            meta=FrontSourceTargetMeta(
                type=FrontSourceTargetMetaType.TEAMMATE
            ),
        ),
    )


def test_front_unassign_event_from_dict():
    assert FrontEvent.from_typed_dict(
        {
            "id": "evt_168gkxxj",
            "type": "unassign",
            "_links": {
                "self": "https://api2.frontapp.com/events/evt_168gkxxj"
            },
            "source": {
                "data": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://api2.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://api2.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://api2.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                },
                "_meta": {"type": "teammate"},
            },
            "emitted_at": 1602125868.188,
            "conversation": {
                "id": "cnv_8p1bfgn",
                "tags": [],
                "_links": {
                    "self": "https://api2.frontapp.com/conversations/cnv_8p1bfgn",
                    "related": {
                        "events": "https://api2.frontapp.com/conversations/cnv_8p1bfgn/events",
                        "inboxes": "https://api2.frontapp.com/conversations/cnv_8p1bfgn/inboxes",
                        "comments": "https://api2.frontapp.com/conversations/cnv_8p1bfgn/comments",
                        "messages": "https://api2.frontapp.com/conversations/cnv_8p1bfgn/messages",
                        "followers": "https://api2.frontapp.com/conversations/cnv_8p1bfgn/followers",
                    },
                },
                "status": "unassigned",
                "subject": "",
                "assignee": None,
                "recipient": {
                    "role": "from",
                    "_links": {
                        "related": {
                            "contact": "https://api2.frontapp.com/contacts/crd_10gex6v"
                        }
                    },
                    "handle": "u-7a23ddb597cb435ebbf60ec1ad311a13",
                },
                "created_at": 1602113126.029,
                "is_private": False,
                "last_message": {
                    "id": "msg_hipi8jr",
                    "body": "Hello, World!",
                    "text": "Hello, World!",
                    "type": "custom",
                    "blurb": "Hello, World!",
                    "_links": {
                        "self": "https://api2.frontapp.com/messages/msg_hipi8jr",
                        "related": {
                            "conversation": "https://api2.frontapp.com/conversations/cnv_8p1bfgn"
                        },
                    },
                    "author": None,
                    "subject": "",
                    "version": None,
                    "is_draft": False,
                    "metadata": {"headers": {}},
                    "created_at": 1602114708.766,
                    "error_type": None,
                    "is_inbound": True,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {
                                "related": {
                                    "contact": "https://api2.frontapp.com/contacts/crd_10gex6v"
                                }
                            },
                            "handle": "u-7a23ddb597cb435ebbf60ec1ad311a13",
                        },
                        {
                            "role": "to",
                            "_links": {"related": {"contact": None}},
                            "handle": "ba490680fd1da827",
                        },
                    ],
                    "attachments": [],
                },
            },
        }
    ) == FrontUnassignEvent(
        source=FrontSourceTargetData(
            data=FrontTeammateGet(
                id="tea_b2c7",
                first_name="Amanie",
                last_name="Ismail",
                email="amanie@meya.ai",
                username="amanie",
                is_admin=True,
                is_available=True,
                is_blocked=False,
                custom_fields={},
            ),
            meta=FrontSourceTargetMeta(
                type=FrontSourceTargetMetaType.TEAMMATE
            ),
        ),
        conversation=FrontConversationGet(
            id="cnv_8p1bfgn", status="unassigned", subject=""
        ),
        emitted_at=1602125868.188,
    )

    assert FrontEvent.from_typed_dict(
        {
            "id": "evt_1ow7wonb",
            "type": "unassign",
            "_links": {
                "self": "https://meya-partner-developer-account.api.frontapp.com/events/evt_1ow7wonb"
            },
            "source": {"data": None, "_meta": {"type": "api"}},
            "emitted_at": 1625758576.764,
            "conversation": {
                "id": "cnv_bewwgnb",
                "tags": [],
                "_links": {
                    "self": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bewwgnb",
                    "related": {
                        "events": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bewwgnb/events",
                        "inboxes": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bewwgnb/inboxes",
                        "comments": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bewwgnb/comments",
                        "messages": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bewwgnb/messages",
                        "followers": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bewwgnb/followers",
                    },
                },
                "status": "unassigned",
                "subject": "Re:",
                "assignee": None,
                "metadata": {},
                "recipient": {
                    "role": "to",
                    "_links": {
                        "related": {
                            "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1rhl9fr"
                        }
                    },
                    "handle": "meya_user/u-b5e9dcb7bdc345e2a13252909b1e988f",
                },
                "created_at": 1625755793.238,
                "is_private": False,
                "last_message": {
                    "id": "msg_peqv37r",
                    "body": "[status: Conversation assigned to agent Loyalty Rewards Bot]",
                    "text": "[status: Conversation assigned to agent Loyalty Rewards Bot]",
                    "type": "custom",
                    "blurb": "[status: Conversation assigned to agent Loyalty Rewards Bot]",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_peqv37r",
                        "related": {
                            "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bewwgnb",
                            "message_replied_to": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_peqv37r/parent",
                        },
                    },
                    "author": {
                        "id": "tea_d0tj",
                        "email": "support@meya.ai",
                        "_links": {
                            "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_d0tj",
                            "related": {
                                "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_d0tj/inboxes",
                                "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_d0tj/conversations",
                            },
                        },
                        "is_admin": True,
                        "username": "support",
                        "last_name": "Bot",
                        "first_name": "Meya",
                        "is_blocked": False,
                        "is_available": True,
                        "custom_fields": {},
                    },
                    "subject": "Re:",
                    "version": None,
                    "is_draft": False,
                    "metadata": {
                        "headers": {
                            "in_reply_to": "external_message_t-b3a3d9a6139e4db4b127f6b83a8ba4e7_msg_peqdl6v@1627152718.ext.frontapp.com"
                        }
                    },
                    "created_at": 1625758312.454,
                    "draft_mode": None,
                    "error_type": None,
                    "is_inbound": False,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {"related": {"contact": None}},
                            "handle": "2bf5b4dac7dcd37b",
                        },
                        {
                            "role": "to",
                            "_links": {
                                "related": {
                                    "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1rhl9fr"
                                }
                            },
                            "handle": "meya_user/u-b5e9dcb7bdc345e2a13252909b1e988f",
                        },
                    ],
                    "attachments": [],
                },
                "scheduled_reminders": [],
            },
        }
    ) == FrontUnassignEvent(
        source=FrontSourceTargetData(
            data=None,
            meta=FrontSourceTargetMeta(type=FrontSourceTargetMetaType.API),
        ),
        conversation=FrontConversationGet(
            id="cnv_bewwgnb", status="unassigned", subject="Re:"
        ),
        emitted_at=1625758576.764,
    )


def test_front_comment_event_from_dict():
    assert FrontEvent.from_typed_dict(
        {
            "id": "evt_168gr0nb",
            "type": "comment",
            "_links": {
                "self": "https://api2.frontapp.com/events/evt_168gr0nb"
            },
            "source": {
                "data": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://api2.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://api2.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://api2.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                },
                "_meta": {"type": "teammate"},
            },
            "target": {
                "data": {
                    "id": "com_lm1jt3",
                    "body": "New comment",
                    "_links": {
                        "self": "https://api2.frontapp.com/comments/com_lm1jt3",
                        "related": {
                            "mentions": "https://api2.frontapp.com/comments/com_lm1jt3/mentions",
                            "conversation": "https://api2.frontapp.com/conversations/cnv_8p1bfgn",
                        },
                    },
                    "author": {
                        "id": "tea_b2c7",
                        "email": "amanie@meya.ai",
                        "_links": {
                            "self": "https://api2.frontapp.com/teammates/tea_b2c7",
                            "related": {
                                "inboxes": "https://api2.frontapp.com/teammates/tea_b2c7/inboxes",
                                "conversations": "https://api2.frontapp.com/teammates/tea_b2c7/conversations",
                            },
                        },
                        "is_admin": True,
                        "username": "amanie",
                        "last_name": "Ismail",
                        "first_name": "Amanie",
                        "is_blocked": False,
                        "is_available": True,
                    },
                    "posted_at": 1602126167.845,
                },
                "_meta": {"type": "comment"},
            },
            "emitted_at": 1602126167.916,
            "conversation": {
                "id": "cnv_8p1bfgn",
                "tags": [],
                "_links": {
                    "self": "https://api2.frontapp.com/conversations/cnv_8p1bfgn",
                    "related": {
                        "events": "https://api2.frontapp.com/conversations/cnv_8p1bfgn/events",
                        "inboxes": "https://api2.frontapp.com/conversations/cnv_8p1bfgn/inboxes",
                        "comments": "https://api2.frontapp.com/conversations/cnv_8p1bfgn/comments",
                        "messages": "https://api2.frontapp.com/conversations/cnv_8p1bfgn/messages",
                        "followers": "https://api2.frontapp.com/conversations/cnv_8p1bfgn/followers",
                    },
                },
                "status": "unassigned",
                "subject": "",
                "assignee": None,
                "recipient": {
                    "role": "from",
                    "_links": {
                        "related": {
                            "contact": "https://api2.frontapp.com/contacts/crd_10gex6v"
                        }
                    },
                    "handle": "u-7a23ddb597cb435ebbf60ec1ad311a13",
                },
                "created_at": 1602113126.029,
                "is_private": False,
                "last_message": {
                    "id": "msg_hipi8jr",
                    "body": "Hello, World!",
                    "text": "Hello, World!",
                    "type": "custom",
                    "blurb": "Hello, World!",
                    "_links": {
                        "self": "https://api2.frontapp.com/messages/msg_hipi8jr",
                        "related": {
                            "conversation": "https://api2.frontapp.com/conversations/cnv_8p1bfgn"
                        },
                    },
                    "author": None,
                    "subject": "",
                    "version": None,
                    "is_draft": False,
                    "metadata": {"headers": {}},
                    "created_at": 1602114708.766,
                    "error_type": None,
                    "is_inbound": True,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {
                                "related": {
                                    "contact": "https://api2.frontapp.com/contacts/crd_10gex6v"
                                }
                            },
                            "handle": "u-7a23ddb597cb435ebbf60ec1ad311a13",
                        },
                        {
                            "role": "to",
                            "_links": {"related": {"contact": None}},
                            "handle": "ba490680fd1da827",
                        },
                    ],
                    "attachments": [],
                },
            },
        }
    ) == FrontCommentEvent(
        conversation=FrontConversationGet(
            id="cnv_8p1bfgn", status="unassigned", subject=""
        ),
        emitted_at=1602126167.916,
        target=FrontEventCommentData(
            data=FrontCommentGet(
                author=FrontTeammateGet(
                    email="amanie@meya.ai",
                    first_name="Amanie",
                    id="tea_b2c7",
                    last_name="Ismail",
                    username="amanie",
                    is_admin=True,
                    is_available=True,
                    is_blocked=False,
                ),
                body="New comment",
            )
        ),
    )


@pytest.mark.parametrize(
    ("offset", "is_expired"),
    [
        (timedelta(), False),
        (timedelta(minutes=-4), False),
        (timedelta(minutes=+4), False),
        (timedelta(minutes=-5), True),
        (timedelta(minutes=+5), True),
        (timedelta(minutes=-6), True),
        (timedelta(minutes=+6), True),
    ],
)
def test_front_event_is_expired(offset: timedelta, is_expired: bool):
    event = FrontActionEvent(
        conversation=MagicMock(),
        emitted_at=frozen_milliseconds_timestamp / 1000.0,
    )
    with freeze_time(
        from_utc_milliseconds_timestamp(frozen_milliseconds_timestamp) + offset
    ):
        assert event.is_expired == is_expired


@pytest.mark.parametrize(
    ("payload", "obj"),
    [
        (
            {
                "type": "message",
                "payload": {
                    "id": "msg_o3p3h53",
                    "body": "Hi",
                    "text": "Hi",
                    "type": "custom",
                    "blurb": "Hi",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_o3p3h53",
                        "related": {
                            "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_az8l7ev",
                            "message_replied_to": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_o3p3h53/parent",
                        },
                    },
                    "author": {
                        "id": "tea_b2c7",
                        "email": "amanie@meya.ai",
                        "_links": {
                            "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                            "related": {
                                "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                                "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                            },
                        },
                        "is_admin": True,
                        "username": "amanie",
                        "last_name": "Ismail",
                        "first_name": "Amanie",
                        "is_blocked": False,
                        "is_available": True,
                    },
                    "subject": "Meya conversation",
                    "version": "66d2906de7de1f2be618d9b8e4b826a2-318607-1622118533048-bf10",
                    "is_draft": True,
                    "metadata": {
                        "headers": {"in_reply_to": "01f7f4ced944516a"}
                    },
                    "created_at": 1622118535.369,
                    "draft_mode": "private",
                    "error_type": None,
                    "is_inbound": False,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {"related": {"contact": None}},
                            "handle": "6e2bc06b7414176e",
                        },
                        {
                            "role": "to",
                            "_links": {"related": {"contact": None}},
                            "handle": "meya_user/u-0208146bf9a64f1788598ffcc511bb5d",
                        },
                    ],
                    "attachments": [],
                },
                "metadata": {
                    "external_conversation_id": "meya_thread/t-f4703088fd5f4d5aa5565d84dbf28cdd",
                    "external_conversation_ids": [
                        "meya_thread/t-f4703088fd5f4d5aa5565d84dbf28cdd"
                    ],
                },
            },
            FrontChannelMessageEvent(
                payload=FrontPartnerChannelMessage(
                    id="msg_o3p3h53",
                    is_inbound=False,
                    body="Hi",
                    links=FrontMessageGetRecipientLinks(
                        related=FrontMessageGetRecipientRelated(
                            conversation="https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_az8l7ev"
                        )
                    ),
                    author=FrontTeammateGet(
                        id="tea_b2c7",
                        email="amanie@meya.ai",
                        first_name="Amanie",
                        last_name="Ismail",
                        username="amanie",
                        is_admin=True,
                        is_available=True,
                        is_blocked=False,
                    ),
                    created_at=1622118535.369,
                    recipients=[
                        FrontMessageGetRecipient(
                            role="from",
                            links=FrontMessageGetRecipientLinks(
                                related=FrontMessageGetRecipientRelated(
                                    contact=None
                                )
                            ),
                            handle="6e2bc06b7414176e",
                        ),
                        FrontMessageGetRecipient(
                            role="to",
                            links=FrontMessageGetRecipientLinks(
                                related=FrontMessageGetRecipientRelated(
                                    contact=None
                                )
                            ),
                            handle="meya_user/u-0208146bf9a64f1788598ffcc511bb5d",
                        ),
                    ],
                    text="Hi",
                    type="custom",
                ),
                metadata=FrontPartnerChannelMetadata(
                    external_conversation_id="meya_thread/t-f4703088fd5f4d5aa5565d84dbf28cdd",
                    external_conversation_ids=[
                        "meya_thread/t-f4703088fd5f4d5aa5565d84dbf28cdd"
                    ],
                ),
            ),
        ),
        (
            {
                "type": "message",
                "payload": {
                    "id": "msg_sc0wr0n",
                    "body": "Test",
                    "text": "Test",
                    "type": "custom",
                    "blurb": "Test",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_sc0wr0n",
                        "related": {
                            "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_cdp0nrb"
                        },
                    },
                    "author": {
                        "id": "tea_b2c7",
                        "email": "amanie@meya.ai",
                        "_links": {
                            "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                            "related": {
                                "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                                "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                            },
                        },
                        "is_admin": True,
                        "username": "amanie",
                        "last_name": "Ismail",
                        "first_name": "Amanie",
                        "is_blocked": False,
                        "is_available": True,
                        "custom_fields": {},
                    },
                    "subject": "",
                    "version": "c26270797b03c728aa0676f8c8f66091-318607-1633473335841-1d24",
                    "is_draft": True,
                    "metadata": {"headers": {"in_reply_to": None}},
                    "created_at": 1633473336.838,
                    "draft_mode": "private",
                    "error_type": None,
                    "is_inbound": False,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {"related": {"contact": None}},
                            "handle": "e354054ec7334ed3",
                        },
                        {
                            "role": "to",
                            "_links": {
                                "related": {
                                    "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1swvd6v"
                                }
                            },
                            "handle": "joao_1990",
                        },
                    ],
                    "attachments": [],
                },
                "metadata": {"external_conversation_ids": []},
            },
            FrontChannelMessageEvent(
                payload=FrontPartnerChannelMessage(
                    id="msg_sc0wr0n",
                    is_inbound=False,
                    body="Test",
                    links=FrontMessageGetRecipientLinks(
                        related=FrontMessageGetRecipientRelated(
                            conversation="https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_cdp0nrb"
                        )
                    ),
                    author=FrontTeammateGet(
                        id="tea_b2c7",
                        email="amanie@meya.ai",
                        first_name="Amanie",
                        last_name="Ismail",
                        username="amanie",
                        is_admin=True,
                        is_available=True,
                        is_blocked=False,
                    ),
                    created_at=1633473336.838,
                    recipients=[
                        FrontMessageGetRecipient(
                            role="from",
                            links=FrontMessageGetRecipientLinks(
                                related=FrontMessageGetRecipientRelated(
                                    contact=None
                                )
                            ),
                            handle="e354054ec7334ed3",
                        ),
                        FrontMessageGetRecipient(
                            role="to",
                            links=FrontMessageGetRecipientLinks(
                                related=FrontMessageGetRecipientRelated(
                                    contact="https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1swvd6v"
                                )
                            ),
                            handle="joao_1990",
                        ),
                    ],
                    text="Test",
                    type="custom",
                ),
                metadata=FrontPartnerChannelMetadata(
                    external_conversation_ids=[]
                ),
            ),
        ),
        (
            {
                "type": "message",
                "payload": {
                    "id": "msg_scop7d3",
                    "body": "Ola",
                    "text": "Ola",
                    "type": "custom",
                    "blurb": "Ola",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_scop7d3",
                        "related": {
                            "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_cdxjpl3"
                        },
                    },
                    "author": {
                        "id": "tea_b2c7",
                        "email": "amanie@meya.ai",
                        "_links": {
                            "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                            "related": {
                                "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                                "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                            },
                        },
                        "is_admin": True,
                        "username": "amanie",
                        "last_name": "Ismail",
                        "first_name": "Amanie",
                        "is_blocked": False,
                        "is_available": True,
                        "custom_fields": {},
                    },
                    "subject": "",
                    "version": "bb0be604fc5ce98b8566251283fdef07-318607-1633528777284-4039",
                    "is_draft": True,
                    "metadata": {"headers": {"in_reply_to": None}},
                    "created_at": 1633528779.311,
                    "draft_mode": "private",
                    "error_type": None,
                    "is_inbound": False,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {"related": {"contact": None}},
                            "handle": "e354054ec7334ed3",
                        },
                        {
                            "role": "to",
                            "_links": {
                                "related": {
                                    "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1swvd6v"
                                }
                            },
                            "handle": "joao_1990",
                        },
                    ],
                    "attachments": [],
                },
                "metadata": {"external_conversation_ids": []},
            },
            FrontChannelMessageEvent(
                payload=FrontPartnerChannelMessage(
                    id="msg_scop7d3",
                    is_inbound=False,
                    body="Ola",
                    links=FrontMessageGetRecipientLinks(
                        related=FrontMessageGetRecipientRelated(
                            conversation="https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_cdxjpl3"
                        )
                    ),
                    author=FrontTeammateGet(
                        id="tea_b2c7",
                        email="amanie@meya.ai",
                        first_name="Amanie",
                        last_name="Ismail",
                        username="amanie",
                        is_admin=True,
                        is_available=True,
                        is_blocked=False,
                    ),
                    created_at=1633528779.311,
                    recipients=[
                        FrontMessageGetRecipient(
                            role="from",
                            links=FrontMessageGetRecipientLinks(
                                related=FrontMessageGetRecipientRelated(
                                    contact=None
                                )
                            ),
                            handle="e354054ec7334ed3",
                        ),
                        FrontMessageGetRecipient(
                            role="to",
                            links=FrontMessageGetRecipientLinks(
                                related=FrontMessageGetRecipientRelated(
                                    contact="https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1swvd6v"
                                )
                            ),
                            handle="joao_1990",
                        ),
                    ],
                    text="Ola",
                    type="custom",
                ),
                metadata=FrontPartnerChannelMetadata(
                    external_conversation_ids=[]
                ),
            ),
        ),
        (
            {
                "type": "message",
                "payload": {
                    "id": "msg_scqpxon",
                    "body": "Hey Hey",
                    "text": "Hey Hey",
                    "type": "custom",
                    "blurb": "Hey Hey",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_scqpxon",
                        "related": {
                            "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_cdy8s7b"
                        },
                    },
                    "author": {
                        "id": "tea_b2c7",
                        "email": "amanie@meya.ai",
                        "_links": {
                            "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                            "related": {
                                "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                                "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                            },
                        },
                        "is_admin": True,
                        "username": "amanie",
                        "last_name": "Ismail",
                        "first_name": "Amanie",
                        "is_blocked": False,
                        "is_available": True,
                        "custom_fields": {},
                    },
                    "subject": "",
                    "version": "734c7bd36b8411d378ee6db0e5dc553c-318607-1633530592526-7bbe",
                    "is_draft": True,
                    "metadata": {"headers": {"in_reply_to": None}},
                    "created_at": 1633530594.181,
                    "draft_mode": "private",
                    "error_type": None,
                    "is_inbound": False,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {"related": {"contact": None}},
                            "handle": "e354054ec7334ed3",
                        },
                        {
                            "role": "to",
                            "_links": {
                                "related": {
                                    "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1q51213"
                                }
                            },
                            "handle": "joao@meya.ai",
                        },
                    ],
                    "attachments": [],
                },
                "metadata": {"external_conversation_ids": []},
            },
            FrontChannelMessageEvent(
                payload=FrontPartnerChannelMessage(
                    id="msg_scqpxon",
                    is_inbound=False,
                    body="Hey Hey",
                    links=FrontMessageGetRecipientLinks(
                        related=FrontMessageGetRecipientRelated(
                            conversation="https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_cdy8s7b"
                        )
                    ),
                    author=FrontTeammateGet(
                        id="tea_b2c7",
                        email="amanie@meya.ai",
                        first_name="Amanie",
                        last_name="Ismail",
                        username="amanie",
                        is_admin=True,
                        is_available=True,
                        is_blocked=False,
                    ),
                    created_at=1633530594.181,
                    recipients=[
                        FrontMessageGetRecipient(
                            role="from",
                            links=FrontMessageGetRecipientLinks(
                                related=FrontMessageGetRecipientRelated(
                                    contact=None
                                )
                            ),
                            handle="e354054ec7334ed3",
                        ),
                        FrontMessageGetRecipient(
                            role="to",
                            links=FrontMessageGetRecipientLinks(
                                related=FrontMessageGetRecipientRelated(
                                    contact="https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1q51213"
                                )
                            ),
                            handle="joao@meya.ai",
                        ),
                    ],
                    text="Hey Hey",
                    type="custom",
                ),
                metadata=FrontPartnerChannelMetadata(
                    external_conversation_ids=[]
                ),
            ),
        ),
    ],
)
def test_front_message_type_partner_channel(payload, obj):
    assert FrontEvent.from_typed_dict(payload) == obj


def test_front_inbound_message():
    assert FrontEvent.from_typed_dict(
        {
            "_links": {
                "self": "https://meya-partner-developer-account.api.frontapp.com/events/evt_1myoplhj"
            },
            "id": "evt_1myoplhj",
            "type": "inbound",
            "emitted_at": 1623417297.368,
            "conversation": {
                "_links": {
                    "self": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b4m29xj",
                    "related": {
                        "events": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b4m29xj/events",
                        "followers": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b4m29xj/followers",
                        "messages": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b4m29xj/messages",
                        "comments": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b4m29xj/comments",
                        "inboxes": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b4m29xj/inboxes",
                    },
                },
                "id": "cnv_b4m29xj",
                "subject": "",
                "status": "unassigned",
                "assignee": None,
                "recipient": {
                    "_links": {"related": {"contact": None}},
                    "handle": "meya_user/u-0d67b56d3c284172a39014becc46c584",
                    "role": "from",
                },
                "tags": [],
                "last_message": {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_okcnmiv",
                        "related": {
                            "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b4m29xj"
                        },
                    },
                    "id": "msg_okcnmiv",
                    "type": "custom",
                    "is_inbound": True,
                    "created_at": 1623417297.368,
                    "blurb": "This is preheader text. Some clients will show this text as a preview. Hi there, Sometimes you just want to send a simple HTML email with a simple design and clear call to action. This is it. Call To ",
                    "body": ' <div>\n  <div>\n    \n    \n    \n  </div>\n  <div class="fa0 front-email-body" style="background-color: #f6f6f6;font-family: sans-serif;-webkit-font-smoothing:\nantialiased;font-size: 14px;line-height: 1.4;margin: 0;padding: 0;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">\n    <span class="fa-b6wcq" style="color: transparent;display: none;height:\n0;max-height: 0;max-width: 0;opacity: 0;overflow: hidden;mso-hide: all;visibility: hidden;width: 0;">This is preheader text. Some clients will show this text as a preview.</span>\n    <table border="0" cellpadding="0" cellspacing="0" class="fa-a30xfy" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;width: 100%;background-color: #f6f6f6;">\n      <tr>\n        <td style="font-family: sans-serif;font-size: 14px;vertical-align:\ntop;">&nbsp;</td>\n        <td class="fa-fn006d" style="font-family: sans-serif;font-size: 14px;vertical-align:\ntop;display: block;max-width: 580px;padding: 10px;width: 580px;margin: 0 auto !important;">\n          <div class="fa-ca79z" style="box-sizing: border-box;display: block;margin:\n0 auto;max-width: 580px;padding: 10px;">\n\n            \n            <table class="fa-hzoal8" style="border-collapse:\nseparate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;width: 100%;background: #ffffff;border-radius: 3px;">\n\n              \n              <tr>\n                <td class="fa-di5dta" style="font-family: sans-serif;font-size:\n14px;vertical-align: top;box-sizing: border-box;padding: 20px;">\n                  <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;width: 100%;">\n                    <tr>\n                      <td style="font-family: sans-serif;font-size: 14px;vertical-align:\ntop;">\n                        <p style="font-family: sans-serif;font-size: 14px;font-weight:\nnormal;margin: 0;margin-bottom: 15px;">Hi there,</p>\n                        <p style="font-family: sans-serif;font-size: 14px;font-weight:\nnormal;margin: 0;margin-bottom: 15px;">Sometimes you just want to send a simple HTML email with a simple design and clear call to action. This is it.</p>\n                        <table border="0" cellpadding="0" cellspacing="0" class="fannz4z5 fa-8rmtz6" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;width: 100%;box-sizing: border-box;">\n                          <tbody>\n                            <tr>\n                              <td align="left" style="font-family: sans-serif;font-size:\n14px;vertical-align: top;padding-bottom: 15px;">\n                                <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;width: auto;">\n                                  <tbody>\n                                    <tr>\n                                      <td style="font-family: sans-serif;font-size:\n14px;vertical-align: top;background-color: #3498db;border-radius: 5px;text-align: center;"> <a href="http://grid.meya.ai/" target="_blank" style="color: #ffffff;text-decoration: none;background-color: #3498db;border: solid 1px #3498db;border-radius: 5px;box-sizing: border-box;cursor: pointer;display: inline-block;font-size: 14px;font-weight: bold;margin: 0;padding: 12px 25px;text-transform: capitalize;border-color: #3498db;" rel="noopener noreferrer">Call To Action</a> </td>\n                                    </tr>\n                                  </tbody>\n                                </table>\n                              </td>\n                            </tr>\n                          </tbody>\n                        </table>\n                        <p style="font-family: sans-serif;font-size: 14px;font-weight:\nnormal;margin: 0;margin-bottom: 15px;">This is a really simple email template. Its sole purpose is to get the recipient to click the button with no distractions.</p>\n                        <p style="font-family: sans-serif;font-size: 14px;font-weight:\nnormal;margin: 0;margin-bottom: 15px;">Good luck! Hope it works.</p>\n                      </td>\n                    </tr>\n                  </table>\n                </td>\n              </tr>\n            \n            </table>\n            \n          </div>\n        </td>\n        <td style="font-family: sans-serif;font-size: 14px;vertical-align:\ntop;">&nbsp;</td>\n      </tr>\n    </table>\n  </div>\n</div>\n',
                    "text": "This is preheader text. Some clients will show this text as a preview. \nHi there,\n\nSometimes you just want to send a simple HTML email with a simple design and clear call to action. This is it.\nCall To Action \n\n\n\n\nThis is a really simple email template. Its sole purpose is to get the recipient to click the button with no distractions.\n\nGood luck! Hope it works.",
                    "error_type": None,
                    "version": None,
                    "subject": "",
                    "draft_mode": None,
                    "metadata": {
                        "thread_ref": "meya_thread/t-50c58b0a27a0452eade2079299459be5"
                    },
                    "author": None,
                    "recipients": [
                        {
                            "_links": {"related": {"contact": None}},
                            "handle": "meya_user/u-0d67b56d3c284172a39014becc46c584",
                            "role": "from",
                        },
                        {
                            "_links": {"related": {"contact": None}},
                            "handle": "e354054ec7334ed3",
                            "role": "to",
                        },
                    ],
                    "attachments": [
                        {
                            "url": "https://meya-partner-developer-account.api.frontapp.com/download/fil_113edp1j",
                            "filename": "300.bin",
                            "content_type": "application/octet-stream",
                            "size": 7183,
                            "metadata": {"is_inline": False},
                        }
                    ],
                    "is_draft": False,
                },
                "created_at": 1623417297.675,
                "is_private": False,
                "scheduled_reminders": [],
                "metadata": {},
            },
            "source": {
                "_meta": {"type": "inboxes"},
                "data": [
                    {
                        "_links": {
                            "self": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d3t3",
                            "related": {
                                "channels": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d3t3/channels",
                                "conversations": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d3t3/conversations",
                                "teammates": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d3t3/teammates",
                                "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                            },
                        },
                        "id": "inb_3d3t3",
                        "name": "Channel Api",
                        "is_private": False,
                        "is_public": False,
                        "address": "e354054ec7334ed3",
                        "send_as": "e354054ec7334ed3",
                        "type": "custom",
                        "custom_fields": {},
                    }
                ],
            },
            "target": {
                "_meta": {"type": "message"},
                "data": {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_okcnmiv",
                        "related": {
                            "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b4m29xj"
                        },
                    },
                    "id": "msg_okcnmiv",
                    "type": "custom",
                    "is_inbound": True,
                    "created_at": 1623417297.368,
                    "blurb": "This is preheader text. Some clients will show this text as a preview. Hi there, Sometimes you just want to send a simple HTML email with a simple design and clear call to action. This is it. Call To ",
                    "body": ' <div>\n  <div>\n    \n    \n    \n  </div>\n  <div class="fa0 front-email-body" style="background-color: #f6f6f6;font-family: sans-serif;-webkit-font-smoothing:\nantialiased;font-size: 14px;line-height: 1.4;margin: 0;padding: 0;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">\n    <span class="fa-b6wcq" style="color: transparent;display: none;height:\n0;max-height: 0;max-width: 0;opacity: 0;overflow: hidden;mso-hide: all;visibility: hidden;width: 0;">This is preheader text. Some clients will show this text as a preview.</span>\n    <table border="0" cellpadding="0" cellspacing="0" class="fa-a30xfy" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;width: 100%;background-color: #f6f6f6;">\n      <tr>\n        <td style="font-family: sans-serif;font-size: 14px;vertical-align:\ntop;">&nbsp;</td>\n        <td class="fa-fn006d" style="font-family: sans-serif;font-size: 14px;vertical-align:\ntop;display: block;max-width: 580px;padding: 10px;width: 580px;margin: 0 auto !important;">\n          <div class="fa-ca79z" style="box-sizing: border-box;display: block;margin:\n0 auto;max-width: 580px;padding: 10px;">\n\n            \n            <table class="fa-hzoal8" style="border-collapse:\nseparate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;width: 100%;background: #ffffff;border-radius: 3px;">\n\n              \n              <tr>\n                <td class="fa-di5dta" style="font-family: sans-serif;font-size:\n14px;vertical-align: top;box-sizing: border-box;padding: 20px;">\n                  <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;width: 100%;">\n                    <tr>\n                      <td style="font-family: sans-serif;font-size: 14px;vertical-align:\ntop;">\n                        <p style="font-family: sans-serif;font-size: 14px;font-weight:\nnormal;margin: 0;margin-bottom: 15px;">Hi there,</p>\n                        <p style="font-family: sans-serif;font-size: 14px;font-weight:\nnormal;margin: 0;margin-bottom: 15px;">Sometimes you just want to send a simple HTML email with a simple design and clear call to action. This is it.</p>\n                        <table border="0" cellpadding="0" cellspacing="0" class="fannz4z5 fa-8rmtz6" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;width: 100%;box-sizing: border-box;">\n                          <tbody>\n                            <tr>\n                              <td align="left" style="font-family: sans-serif;font-size:\n14px;vertical-align: top;padding-bottom: 15px;">\n                                <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;width: auto;">\n                                  <tbody>\n                                    <tr>\n                                      <td style="font-family: sans-serif;font-size:\n14px;vertical-align: top;background-color: #3498db;border-radius: 5px;text-align: center;"> <a href="http://grid.meya.ai/" target="_blank" style="color: #ffffff;text-decoration: none;background-color: #3498db;border: solid 1px #3498db;border-radius: 5px;box-sizing: border-box;cursor: pointer;display: inline-block;font-size: 14px;font-weight: bold;margin: 0;padding: 12px 25px;text-transform: capitalize;border-color: #3498db;" rel="noopener noreferrer">Call To Action</a> </td>\n                                    </tr>\n                                  </tbody>\n                                </table>\n                              </td>\n                            </tr>\n                          </tbody>\n                        </table>\n                        <p style="font-family: sans-serif;font-size: 14px;font-weight:\nnormal;margin: 0;margin-bottom: 15px;">This is a really simple email template. Its sole purpose is to get the recipient to click the button with no distractions.</p>\n                        <p style="font-family: sans-serif;font-size: 14px;font-weight:\nnormal;margin: 0;margin-bottom: 15px;">Good luck! Hope it works.</p>\n                      </td>\n                    </tr>\n                  </table>\n                </td>\n              </tr>\n            \n            </table>\n            \n          </div>\n        </td>\n        <td style="font-family: sans-serif;font-size: 14px;vertical-align:\ntop;">&nbsp;</td>\n      </tr>\n    </table>\n  </div>\n</div>\n',
                    "text": "This is preheader text. Some clients will show this text as a preview. \nHi there,\n\nSometimes you just want to send a simple HTML email with a simple design and clear call to action. This is it.\nCall To Action \n\n\n\n\nThis is a really simple email template. Its sole purpose is to get the recipient to click the button with no distractions.\n\nGood luck! Hope it works.",
                    "error_type": None,
                    "version": None,
                    "subject": "",
                    "draft_mode": None,
                    "metadata": {
                        "thread_ref": "meya_thread/t-50c58b0a27a0452eade2079299459be5"
                    },
                    "author": None,
                    "recipients": [
                        {
                            "_links": {"related": {"contact": None}},
                            "handle": "meya_user/u-0d67b56d3c284172a39014becc46c584",
                            "role": "from",
                        },
                        {
                            "_links": {"related": {"contact": None}},
                            "handle": "e354054ec7334ed3",
                            "role": "to",
                        },
                    ],
                    "attachments": [
                        {
                            "url": "https://meya-partner-developer-account.api.frontapp.com/download/fil_113edp1j",
                            "filename": "300.bin",
                            "content_type": "application/octet-stream",
                            "size": 7183,
                            "metadata": {"is_inline": False},
                        }
                    ],
                    "is_draft": False,
                },
            },
        }
    )


def test_front_tag_event():
    assert FrontEvent.from_typed_dict(
        {
            "id": "evt_1nqmx5hj",
            "type": "tag",
            "_links": {
                "self": "https://meya-partner-developer-account.api.frontapp.com/events/evt_1nqmx5hj"
            },
            "source": {
                "data": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                    "custom_fields": {},
                },
                "_meta": {"type": "teammate"},
            },
            "target": {
                "data": {
                    "id": "tag_u2b47",
                    "name": "Bounces",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/tags/tag_u2b47",
                        "related": {
                            "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                            "children": None,
                            "parent_tag": None,
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/tags/tag_u2b47/conversations",
                        },
                    },
                    "highlight": None,
                    "created_at": 1614885295.042,
                    "is_private": False,
                    "updated_at": 1624387401.59,
                },
                "_meta": {"type": "tag"},
            },
            "emitted_at": 1624387405.264,
            "conversation": {
                "id": "cnv_b84agp3",
                "tags": [],
                "_links": {
                    "self": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b84agp3",
                    "related": {
                        "events": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b84agp3/events",
                        "inboxes": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b84agp3/inboxes",
                        "comments": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b84agp3/comments",
                        "messages": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b84agp3/messages",
                        "followers": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b84agp3/followers",
                    },
                },
                "status": "assigned",
                "subject": "Re: ",
                "assignee": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                    "custom_fields": {},
                },
                "metadata": {},
                "recipient": {
                    "role": "to",
                    "_links": {
                        "related": {
                            "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1qzuhtz"
                        }
                    },
                    "handle": "meya_user/u-066139aa5c874aca891e7138a5063e17",
                },
                "created_at": 1624279479.062,
                "is_private": False,
                "last_message": {
                    "id": "msg_ouk1ldz",
                    "body": "Hello",
                    "text": "Hello",
                    "type": "custom",
                    "blurb": "Hello",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_ouk1ldz",
                        "related": {
                            "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b84agp3",
                            "message_replied_to": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_ouk1ldz/parent",
                        },
                    },
                    "author": {
                        "id": "tea_b2c7",
                        "email": "amanie@meya.ai",
                        "_links": {
                            "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                            "related": {
                                "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                                "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                            },
                        },
                        "is_admin": True,
                        "username": "amanie",
                        "last_name": "Ismail",
                        "first_name": "Amanie",
                        "is_blocked": False,
                        "is_available": True,
                        "custom_fields": {},
                    },
                    "subject": "",
                    "version": None,
                    "is_draft": False,
                    "metadata": {
                        "headers": {"in_reply_to": "c109cccd0fff1b07"}
                    },
                    "created_at": 1624280818.335,
                    "draft_mode": None,
                    "error_type": None,
                    "is_inbound": False,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {"related": {"contact": None}},
                            "handle": "e354054ec7334ed3",
                        },
                        {
                            "role": "to",
                            "_links": {
                                "related": {
                                    "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1qzuhtz"
                                }
                            },
                            "handle": "meya_user/u-066139aa5c874aca891e7138a5063e17",
                        },
                    ],
                    "attachments": [],
                },
                "scheduled_reminders": [],
            },
        }
    ) == FrontTagEvent(
        emitted_at=1624387405.264,
        conversation=FrontConversationGet(
            assignee=FrontTeammateGet(
                id="tea_b2c7",
                first_name="Amanie",
                email="amanie@meya.ai",
                custom_fields={},
                last_name="Ismail",
                username="amanie",
                is_admin=True,
                is_available=True,
                is_blocked=False,
            ),
            id="cnv_b84agp3",
            status="assigned",
            subject="Re: ",
        ),
        target=FrontTagTarget(
            data=FrontTagTargetData(id="tag_u2b47", name="Bounces")
        ),
        source=FrontSourceTargetData(
            data=FrontTeammateGet(
                id="tea_b2c7",
                first_name="Amanie",
                email="amanie@meya.ai",
                custom_fields={},
                last_name="Ismail",
                username="amanie",
                is_admin=True,
                is_available=True,
                is_blocked=False,
            ),
            meta=FrontSourceTargetMeta(
                type=FrontSourceTargetMetaType.TEAMMATE
            ),
        ),
    )


def test_front_untag_event():
    assert FrontEvent.from_typed_dict(
        {
            "id": "evt_1nqmx5hj",
            "type": "untag",
            "_links": {
                "self": "https://meya-partner-developer-account.api.frontapp.com/events/evt_1nqmx5hj"
            },
            "source": {
                "data": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                    "custom_fields": {},
                },
                "_meta": {"type": "teammate"},
            },
            "target": {
                "data": {
                    "id": "tag_u2b47",
                    "name": "Bounces",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/tags/tag_u2b47",
                        "related": {
                            "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                            "children": None,
                            "parent_tag": None,
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/tags/tag_u2b47/conversations",
                        },
                    },
                    "highlight": None,
                    "created_at": 1614885295.042,
                    "is_private": False,
                    "updated_at": 1624387401.59,
                },
                "_meta": {"type": "tag"},
            },
            "emitted_at": 1624387405.264,
            "conversation": {
                "id": "cnv_b84agp3",
                "tags": [],
                "_links": {
                    "self": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b84agp3",
                    "related": {
                        "events": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b84agp3/events",
                        "inboxes": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b84agp3/inboxes",
                        "comments": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b84agp3/comments",
                        "messages": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b84agp3/messages",
                        "followers": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b84agp3/followers",
                    },
                },
                "status": "assigned",
                "subject": "Re: ",
                "assignee": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                    "custom_fields": {},
                },
                "metadata": {},
                "recipient": {
                    "role": "to",
                    "_links": {
                        "related": {
                            "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1qzuhtz"
                        }
                    },
                    "handle": "meya_user/u-066139aa5c874aca891e7138a5063e17",
                },
                "created_at": 1624279479.062,
                "is_private": False,
                "last_message": {
                    "id": "msg_ouk1ldz",
                    "body": "Hello",
                    "text": "Hello",
                    "type": "custom",
                    "blurb": "Hello",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_ouk1ldz",
                        "related": {
                            "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b84agp3",
                            "message_replied_to": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_ouk1ldz/parent",
                        },
                    },
                    "author": {
                        "id": "tea_b2c7",
                        "email": "amanie@meya.ai",
                        "_links": {
                            "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                            "related": {
                                "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                                "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                            },
                        },
                        "is_admin": True,
                        "username": "amanie",
                        "last_name": "Ismail",
                        "first_name": "Amanie",
                        "is_blocked": False,
                        "is_available": True,
                        "custom_fields": {},
                    },
                    "subject": "",
                    "version": None,
                    "is_draft": False,
                    "metadata": {
                        "headers": {"in_reply_to": "c109cccd0fff1b07"}
                    },
                    "created_at": 1624280818.335,
                    "draft_mode": None,
                    "error_type": None,
                    "is_inbound": False,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {"related": {"contact": None}},
                            "handle": "e354054ec7334ed3",
                        },
                        {
                            "role": "to",
                            "_links": {
                                "related": {
                                    "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1qzuhtz"
                                }
                            },
                            "handle": "meya_user/u-066139aa5c874aca891e7138a5063e17",
                        },
                    ],
                    "attachments": [],
                },
                "scheduled_reminders": [],
            },
        }
    ) == FrontUntagEvent(
        emitted_at=1624387405.264,
        conversation=FrontConversationGet(
            assignee=FrontTeammateGet(
                id="tea_b2c7",
                first_name="Amanie",
                email="amanie@meya.ai",
                custom_fields={},
                last_name="Ismail",
                username="amanie",
                is_admin=True,
                is_available=True,
                is_blocked=False,
            ),
            id="cnv_b84agp3",
            status="assigned",
            subject="Re: ",
        ),
        target=FrontTagTarget(
            data=FrontTagTargetData(id="tag_u2b47", name="Bounces")
        ),
        source=FrontSourceTargetData(
            data=FrontTeammateGet(
                id="tea_b2c7",
                first_name="Amanie",
                email="amanie@meya.ai",
                custom_fields={},
                last_name="Ismail",
                username="amanie",
                is_admin=True,
                is_available=True,
                is_blocked=False,
            ),
            meta=FrontSourceTargetMeta(
                type=FrontSourceTargetMetaType.TEAMMATE
            ),
        ),
    )


def test_front_trash_event():
    assert FrontEvent.from_typed_dict(
        {
            "id": "evt_1nqescw7",
            "type": "trash",
            "_links": {
                "self": "https://meya-partner-developer-account.api.frontapp.com/events/evt_1nqescw7"
            },
            "source": {
                "data": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                    "custom_fields": {},
                },
                "_meta": {"type": "teammate"},
            },
            "emitted_at": 1624384549.123,
            "conversation": {
                "id": "cnv_b7lx0nb",
                "tags": [],
                "_links": {
                    "self": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b7lx0nb",
                    "related": {
                        "events": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b7lx0nb/events",
                        "inboxes": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b7lx0nb/inboxes",
                        "comments": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b7lx0nb/comments",
                        "messages": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b7lx0nb/messages",
                        "followers": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b7lx0nb/followers",
                    },
                },
                "status": "deleted",
                "subject": "Custom conversation with meya_user/u-1c864a907b754058b77d60993df16a33",
                "assignee": None,
                "metadata": {},
                "recipient": {
                    "role": "from",
                    "_links": {
                        "related": {
                            "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1qyb64n"
                        }
                    },
                    "handle": "meya_user/u-1c864a907b754058b77d60993df16a33",
                },
                "created_at": 1624049544.189,
                "is_private": False,
                "last_message": {
                    "id": "msg_ot5bflz",
                    "body": ' <div>\n  <div>\n    \n    \n    \n  </div>\n  <div class="fa0 front-email-body" style="background-color: #f6f6f6;font-family: sans-serif;-webkit-font-smoothing:\nantialiased;font-size: 14px;line-height: 1.4;margin: 0;padding: 0;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">\n    <span class="fa-b6wcq" style="color: transparent;display: none;height:\n0;max-height: 0;max-width: 0;opacity: 0;overflow: hidden;mso-hide: all;visibility: hidden;width: 0;">This is preheader text. Some clients will show this text as a preview.</span>\n    <table border="0" cellpadding="0" cellspacing="0" class="fa-a30xfy" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;width: 100%;background-color: #f6f6f6;">\n      <tr>\n        <td style="font-family: sans-serif;font-size: 14px;vertical-align:\ntop;">&nbsp;</td>\n        <td class="fa-fn006d" style="font-family: sans-serif;font-size: 14px;vertical-align:\ntop;display: block;max-width: 580px;padding: 10px;width: 580px;margin: 0 auto !important;">\n          <div class="fa-ca79z" style="box-sizing: border-box;display: block;margin:\n0 auto;max-width: 580px;padding: 10px;">\n\n            \n            <table class="fa-hzoal8" style="border-collapse:\nseparate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;width: 100%;background: #ffffff;border-radius: 3px;">\n\n              \n              <tr>\n                <td class="fa-di5dta" style="font-family: sans-serif;font-size:\n14px;vertical-align: top;box-sizing: border-box;padding: 20px;">\n                  <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;width: 100%;">\n                    <tr>\n                      <td style="font-family: sans-serif;font-size: 14px;vertical-align:\ntop;">\n                        <p style="font-family: sans-serif;font-size: 14px;font-weight:\nnormal;margin: 0;margin-bottom: 15px;">Hi there,</p>\n                        <p style="font-family: sans-serif;font-size: 14px;font-weight:\nnormal;margin: 0;margin-bottom: 15px;">Sometimes you just want to send a simple HTML email with a simple design and clear call to action. This is it.</p>\n                        <table border="0" cellpadding="0" cellspacing="0" class="fannz4z5 fa-8rmtz6" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;width: 100%;box-sizing: border-box;">\n                          <tbody>\n                            <tr>\n                              <td align="left" style="font-family: sans-serif;font-size:\n14px;vertical-align: top;padding-bottom: 15px;">\n                                <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: separate;mso-table-lspace: 0pt;mso-table-rspace: 0pt;width: auto;">\n                                  <tbody>\n                                    <tr>\n                                      <td style="font-family: sans-serif;font-size:\n14px;vertical-align: top;background-color: #3498db;border-radius: 5px;text-align: center;"> <a href="http://grid.meya.ai/" target="_blank" style="color: #ffffff;text-decoration: none;background-color: #3498db;border: solid 1px #3498db;border-radius: 5px;box-sizing: border-box;cursor: pointer;display: inline-block;font-size: 14px;font-weight: bold;margin: 0;padding: 12px 25px;text-transform: capitalize;border-color: #3498db;" rel="noopener noreferrer">Call To Action</a> </td>\n                                    </tr>\n                                  </tbody>\n                                </table>\n                              </td>\n                            </tr>\n                          </tbody>\n                        </table>\n                        <p style="font-family: sans-serif;font-size: 14px;font-weight:\nnormal;margin: 0;margin-bottom: 15px;">This is a really simple email template. Its sole purpose is to get the recipient to click the button with no distractions.</p>\n                        <p style="font-family: sans-serif;font-size: 14px;font-weight:\nnormal;margin: 0;margin-bottom: 15px;">Good luck! Hope it works.</p>\n                      </td>\n                    </tr>\n                  </table>\n                </td>\n              </tr>\n            \n            </table>\n            \n          </div>\n        </td>\n        <td style="font-family: sans-serif;font-size: 14px;vertical-align:\ntop;">&nbsp;</td>\n      </tr>\n    </table>\n  </div>\n</div>\n',
                    "text": "This is preheader text. Some clients will show this text as a preview. \nHi there,\n\nSometimes you just want to send a simple HTML email with a simple design and clear call to action. This is it.\nCall To Action \n\n\n\n\nThis is a really simple email template. Its sole purpose is to get the recipient to click the button with no distractions.\n\nGood luck! Hope it works.",
                    "type": "custom",
                    "blurb": "This is preheader text. Some clients will show this text as a preview. Hi there, Sometimes you just want to send a simple HTML email with a simple design and clear call to action. This is it. Call To ",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_ot5bflz",
                        "related": {
                            "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b7lx0nb"
                        },
                    },
                    "author": None,
                    "subject": "",
                    "version": None,
                    "is_draft": False,
                    "metadata": {"thread_ref": "meya_thread/ex3333"},
                    "created_at": 1624049543.989,
                    "draft_mode": None,
                    "error_type": None,
                    "is_inbound": True,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {
                                "related": {
                                    "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1qyb64n"
                                }
                            },
                            "handle": "meya_user/u-1c864a907b754058b77d60993df16a33",
                        },
                        {
                            "role": "to",
                            "_links": {"related": {"contact": None}},
                            "handle": "e354054ec7334ed3",
                        },
                    ],
                    "attachments": [],
                },
                "scheduled_reminders": [],
            },
        }
    ) == FrontTrashConversationEvent(
        emitted_at=1624384549.123,
        conversation=FrontConversationGet(
            id="cnv_b7lx0nb",
            status="deleted",
            subject="Custom conversation with meya_user/u-1c864a907b754058b77d60993df16a33",
        ),
        source=FrontSourceTargetData(
            data=FrontTeammateGet(
                id="tea_b2c7",
                email="amanie@meya.ai",
                is_admin=True,
                username="amanie",
                last_name="Ismail",
                first_name="Amanie",
                is_blocked=False,
                is_available=True,
                custom_fields={},
            ),
            meta=FrontSourceTargetMeta(
                type=FrontSourceTargetMetaType.TEAMMATE
            ),
        ),
    )


def test_front_reopen_event():
    assert FrontEvent.from_typed_dict(
        {
            "id": "evt_1p6qkshz",
            "type": "reopen",
            "_links": {
                "self": "https://meya-partner-developer-account.api.frontapp.com/events/evt_1p6qkshz"
            },
            "source": {
                "data": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                    "custom_fields": {},
                },
                "_meta": {"type": "teammate"},
            },
            "emitted_at": 1626138696.249,
            "conversation": {
                "id": "cnv_b3na1af",
                "tags": [],
                "_links": {
                    "self": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b3na1af",
                    "related": {
                        "events": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b3na1af/events",
                        "inboxes": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b3na1af/inboxes",
                        "comments": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b3na1af/comments",
                        "messages": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b3na1af/messages",
                        "followers": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_b3na1af/followers",
                    },
                },
                "status": "assigned",
                "subject": "",
                "assignee": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                    "custom_fields": {},
                },
                "metadata": {},
                "recipient": {
                    "role": "to",
                    "_links": {
                        "related": {
                            "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1q51213"
                        }
                    },
                    "handle": "joao@meya.ai",
                },
                "created_at": 1623246149.658,
                "is_private": False,
                "last_message": {},
                "scheduled_reminders": [],
            },
        }
    ) == FrontReopenConversationEvent(
        emitted_at=1626138696.249,
        conversation=FrontConversationGet(
            id="cnv_b3na1af",
            status="assigned",
            subject="",
            assignee=FrontTeammateGet(
                id="tea_b2c7",
                email="amanie@meya.ai",
                is_admin=True,
                username="amanie",
                last_name="Ismail",
                first_name="Amanie",
                is_blocked=False,
                is_available=True,
                custom_fields={},
            ),
        ),
        source=FrontSourceTargetData(
            data=FrontTeammateGet(
                id="tea_b2c7",
                email="amanie@meya.ai",
                is_admin=True,
                username="amanie",
                last_name="Ismail",
                first_name="Amanie",
                is_blocked=False,
                is_available=True,
                custom_fields={},
            ),
            meta=FrontSourceTargetMeta(
                type=FrontSourceTargetMetaType.TEAMMATE
            ),
        ),
    )


def test_front_restore_event():
    assert FrontEvent.from_typed_dict(
        {
            "id": "evt_1p6rjvwn",
            "type": "restore",
            "_links": {
                "self": "https://meya-partner-developer-account.api.frontapp.com/events/evt_1p6rjvwn"
            },
            "source": {
                "data": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                    "custom_fields": {},
                },
                "_meta": {"type": "teammate"},
            },
            "emitted_at": 1626139835.566,
            "conversation": {
                "id": "cnv_bemephj",
                "tags": [],
                "_links": {
                    "self": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bemephj",
                    "related": {
                        "events": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bemephj/events",
                        "inboxes": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bemephj/inboxes",
                        "comments": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bemephj/comments",
                        "messages": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bemephj/messages",
                        "followers": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bemephj/followers",
                    },
                },
                "status": "assigned",
                "subject": "Re: ",
                "assignee": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                    "custom_fields": {},
                },
                "metadata": {},
                "recipient": {
                    "role": "from",
                    "_links": {
                        "related": {
                            "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1rehvwn"
                        }
                    },
                    "handle": "meya_user/u-1825ede402f94f2bb9f1568bbc3d740a",
                },
                "created_at": 1625686758.636,
                "is_private": False,
                "last_message": {
                    "id": "msg_pduprnr",
                    "body": "<p>front_create_conversation</p>\n",
                    "text": "front_create_conversation",
                    "type": "custom",
                    "blurb": "front_create_conversation",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_pduprnr",
                        "related": {
                            "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bemephj"
                        },
                    },
                    "author": None,
                    "subject": "",
                    "version": None,
                    "is_draft": False,
                    "metadata": {"thread_ref": "meya_thread/crd_1rehvbb_talk"},
                    "created_at": 1625687377.529,
                    "draft_mode": None,
                    "error_type": None,
                    "is_inbound": True,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {
                                "related": {
                                    "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1rehvwn"
                                }
                            },
                            "handle": "meya_user/u-1825ede402f94f2bb9f1568bbc3d740a",
                        },
                        {
                            "role": "to",
                            "_links": {"related": {"contact": None}},
                            "handle": "e354054ec7334ed3",
                        },
                    ],
                    "attachments": [],
                },
                "scheduled_reminders": [],
            },
        }
    ) == FrontRestoreConversationEvent(
        emitted_at=1626139835.566,
        conversation=FrontConversationGet(
            id="cnv_bemephj",
            status="assigned",
            subject="Re: ",
            assignee=FrontTeammateGet(
                id="tea_b2c7",
                email="amanie@meya.ai",
                is_admin=True,
                username="amanie",
                last_name="Ismail",
                first_name="Amanie",
                is_blocked=False,
                is_available=True,
                custom_fields={},
            ),
        ),
        source=FrontSourceTargetData(
            data=FrontTeammateGet(
                id="tea_b2c7",
                email="amanie@meya.ai",
                is_admin=True,
                username="amanie",
                last_name="Ismail",
                first_name="Amanie",
                is_blocked=False,
                is_available=True,
                custom_fields={},
            ),
            meta=FrontSourceTargetMeta(
                type=FrontSourceTargetMetaType.TEAMMATE
            ),
        ),
    )


def test_front_unassign_by_api():
    assert FrontEvent.from_typed_dict(
        {
            "id": "evt_1p7tl70n",
            "type": "unassign",
            "_links": {
                "self": "https://meya-partner-developer-account.api.frontapp.com/events/evt_1p7tl70n"
            },
            "source": {"data": None, "_meta": {"type": "api"}},
            "emitted_at": 1626187762.516,
            "conversation": {
                "id": "cnv_bgneqh3",
                "tags": [],
                "_links": {
                    "self": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bgneqh3",
                    "related": {
                        "events": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bgneqh3/events",
                        "inboxes": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bgneqh3/inboxes",
                        "comments": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bgneqh3/comments",
                        "messages": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bgneqh3/messages",
                        "followers": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bgneqh3/followers",
                    },
                },
                "status": "unassigned",
                "subject": "Re: ",
                "assignee": None,
                "metadata": {},
                "recipient": {
                    "role": "from",
                    "_links": {
                        "related": {
                            "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1rm87pj"
                        }
                    },
                    "handle": "meya_user/u-637a8df160f7452bafd001cbc28f6348",
                },
                "created_at": 1626187640.086,
                "is_private": False,
                "last_message": {
                    "id": "msg_pjwgnrb",
                    "body": "<p>front_update_conversation</p>\n",
                    "text": "front_update_conversation",
                    "type": "custom",
                    "blurb": "front_update_conversation",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_pjwgnrb",
                        "related": {
                            "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bgneqh3"
                        },
                    },
                    "author": None,
                    "subject": "",
                    "version": None,
                    "is_draft": False,
                    "metadata": {
                        "thread_ref": "meya_thread/t-1062d5a3825f4de6a14b6b72d369c305"
                    },
                    "created_at": 1626187761.051,
                    "draft_mode": None,
                    "error_type": None,
                    "is_inbound": True,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {
                                "related": {
                                    "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1rm87pj"
                                }
                            },
                            "handle": "meya_user/u-637a8df160f7452bafd001cbc28f6348",
                        },
                        {
                            "role": "to",
                            "_links": {"related": {"contact": None}},
                            "handle": "e354054ec7334ed3",
                        },
                    ],
                    "attachments": [],
                },
                "scheduled_reminders": [],
            },
        }
    ) == FrontUnassignEvent(
        emitted_at=1626187762.516,
        conversation=FrontConversationGet(
            id="cnv_bgneqh3",
            status="unassigned",
            subject="Re: ",
            assignee=None,
        ),
        source=FrontSourceTargetData(
            data=None,
            meta=FrontSourceTargetMeta(type=FrontSourceTargetMetaType.API),
        ),
    )


def test_front_add_tag_rule_source():
    assert FrontEvent.from_typed_dict(
        {
            "id": "evt_1p44ln2f",
            "type": "tag",
            "_links": {
                "self": "https://meya-partner-developer-account.api.frontapp.com/events/evt_1p44ln2f"
            },
            "source": {
                "data": {
                    "id": "rul_21ivb",
                    "name": "Front Demo [dan] archive tag",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/rules/rul_21ivb",
                        "related": {
                            "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv"
                        },
                    },
                    "actions": ["Tag with HIGH PRIORITY"],
                    "is_private": False,
                },
                "_meta": {"type": "rule"},
            },
            "target": {
                "data": {
                    "id": "tag_x11jb",
                    "name": "HIGH PRIORITY",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/tags/tag_x11jb",
                        "related": {
                            "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                            "children": None,
                            "parent_tag": None,
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/tags/tag_x11jb/conversations",
                        },
                    },
                    "highlight": "red",
                    "created_at": 1625778915.58,
                    "is_private": False,
                    "updated_at": 1626099578.328,
                },
                "_meta": {"type": "tag"},
            },
            "emitted_at": 1626099577.776,
            "conversation": {
                "id": "cnv_bg325zb",
                "tags": [
                    {
                        "id": "tag_x11jb",
                        "name": "HIGH PRIORITY",
                        "_links": {
                            "self": "https://meya-partner-developer-account.api.frontapp.com/tags/tag_x11jb",
                            "related": {
                                "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                                "children": None,
                                "parent_tag": None,
                                "conversations": "https://meya-partner-developer-account.api.frontapp.com/tags/tag_x11jb/conversations",
                            },
                        },
                        "highlight": "red",
                        "created_at": 1625778915.58,
                        "is_private": False,
                        "updated_at": 1626099578.328,
                    }
                ],
                "_links": {
                    "self": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bg325zb",
                    "related": {
                        "events": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bg325zb/events",
                        "inboxes": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bg325zb/inboxes",
                        "comments": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bg325zb/comments",
                        "messages": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bg325zb/messages",
                        "followers": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bg325zb/followers",
                    },
                },
                "status": "assigned",
                "subject": "Re: y",
                "assignee": {
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "is_admin": True,
                    "username": "amanie",
                    "last_name": "Ismail",
                    "first_name": "Amanie",
                    "is_blocked": False,
                    "is_available": True,
                    "custom_fields": {},
                },
                "metadata": {},
                "recipient": {
                    "role": "to",
                    "_links": {
                        "related": {
                            "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1rimqmf"
                        }
                    },
                    "handle": "meya_user/u-0a5fdbc541634f09b77222f0e1edbd10",
                },
                "created_at": 1626098013.979,
                "is_private": False,
                "last_message": {
                    "id": "msg_pi8wqrr",
                    "body": "Sorry, I don't understand. Would you like to talk to customer support?\n--&gt; [Yes]\n--&gt; [No thanks]",
                    "text": "Sorry, I don't understand. Would you like to talk to customer support?\n--> [Yes]\n--> [No thanks]",
                    "type": "custom",
                    "blurb": "Sorry, I don't understand. Would you like to talk to customer support? --> [Yes] --> [No thanks]",
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_pi8wqrr",
                        "related": {
                            "conversation": "https://meya-partner-developer-account.api.frontapp.com/conversations/cnv_bg325zb",
                            "message_replied_to": "https://meya-partner-developer-account.api.frontapp.com/messages/msg_pi8wqrr/parent",
                        },
                    },
                    "author": {
                        "id": "tea_d0tj",
                        "email": "support@meya.ai",
                        "_links": {
                            "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_d0tj",
                            "related": {
                                "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_d0tj/inboxes",
                                "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_d0tj/conversations",
                            },
                        },
                        "is_admin": True,
                        "username": "support",
                        "last_name": "Bot",
                        "first_name": "Meya",
                        "is_blocked": False,
                        "is_available": True,
                        "custom_fields": {},
                    },
                    "subject": "Re: y",
                    "version": None,
                    "is_draft": False,
                    "metadata": {
                        "headers": {"in_reply_to": "2541f14760a95a83"}
                    },
                    "created_at": 1626099009.069,
                    "draft_mode": None,
                    "error_type": None,
                    "is_inbound": False,
                    "recipients": [
                        {
                            "role": "from",
                            "_links": {"related": {"contact": None}},
                            "handle": "250f497436763e7a",
                        },
                        {
                            "role": "to",
                            "_links": {
                                "related": {
                                    "contact": "https://meya-partner-developer-account.api.frontapp.com/contacts/crd_1rimqmf"
                                }
                            },
                            "handle": "meya_user/u-0a5fdbc541634f09b77222f0e1edbd10",
                        },
                    ],
                    "attachments": [],
                },
                "scheduled_reminders": [],
            },
        }
    ) == FrontTagEvent(
        emitted_at=1626099577.776,
        conversation=FrontConversationGet(
            id="cnv_bg325zb",
            status="assigned",
            subject="Re: y",
            assignee=FrontTeammateGet(
                id="tea_b2c7",
                email="amanie@meya.ai",
                is_admin=True,
                username="amanie",
                last_name="Ismail",
                first_name="Amanie",
                is_blocked=False,
                is_available=True,
                custom_fields={},
            ),
        ),
        target=FrontTagTarget(
            data=FrontTagTargetData(id="tag_x11jb", name="HIGH PRIORITY")
        ),
        source=FrontSourceTargetData(
            data=FrontRule(
                id="rul_21ivb",
                name="Front Demo [dan] archive tag",
                is_private=False,
                actions=["Tag with HIGH PRIORITY"],
            ),
            meta=FrontSourceTargetMeta(type=FrontSourceTargetMetaType.RULE),
        ),
    )
