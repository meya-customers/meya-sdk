from meya.front.payload.payload import FrontPagination
from meya.front.payload.teammate import FrontTeammateGet
from meya.front.payload.teams import FrontInbox
from meya.front.payload.teams import FrontInboxLinks
from meya.front.payload.teams import FrontInboxLinksRelated
from meya.front.payload.teams import FrontTeam
from meya.front.payload.teams import FrontTeams
from meya.front.payload.teams import FrontTeamsData


def test_front_team():
    assert FrontTeam.from_dict(
        {
            "_links": {
                "self": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv"
            },
            "id": "tim_6xuv",
            "name": "Meya Partner Developer Account",
            "inboxes": [
                {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_326dj",
                        "related": {
                            "channels": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_326dj/channels",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_326dj/conversations",
                            "teammates": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_326dj/teammates",
                            "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                        },
                    },
                    "id": "inb_326dj",
                    "name": "Front + Meya [test]",
                    "is_private": False,
                    "is_public": False,
                    "custom_fields": {},
                },
                {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_368ef",
                        "related": {
                            "channels": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_368ef/channels",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_368ef/conversations",
                            "teammates": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_368ef/teammates",
                            "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                        },
                    },
                    "id": "inb_368ef",
                    "name": "Seal Team 6",
                    "is_private": False,
                    "is_public": False,
                    "custom_fields": {},
                },
                {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_39ifb",
                        "related": {
                            "channels": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_39ifb/channels",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_39ifb/conversations",
                            "teammates": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_39ifb/teammates",
                            "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                        },
                    },
                    "id": "inb_39ifb",
                    "name": "Priority inbox",
                    "is_private": False,
                    "is_public": False,
                    "custom_fields": {},
                },
                {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_39ukn",
                        "related": {
                            "channels": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_39ukn/channels",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_39ukn/conversations",
                            "teammates": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_39ukn/teammates",
                            "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                        },
                    },
                    "id": "inb_39ukn",
                    "name": "Harley",
                    "is_private": False,
                    "is_public": False,
                    "custom_fields": {},
                },
                {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3c98n",
                        "related": {
                            "channels": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3c98n/channels",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3c98n/conversations",
                            "teammates": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3c98n/teammates",
                            "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                        },
                    },
                    "id": "inb_3c98n",
                    "name": "Front Demo",
                    "is_private": False,
                    "is_public": False,
                    "custom_fields": {},
                },
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
                    "custom_fields": {},
                },
                {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d9vr",
                        "related": {
                            "channels": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d9vr/channels",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d9vr/conversations",
                            "teammates": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d9vr/teammates",
                            "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                        },
                    },
                    "id": "inb_3d9vr",
                    "name": "Disney",
                    "is_private": False,
                    "is_public": True,
                    "custom_fields": {},
                },
                {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3ddon",
                        "related": {
                            "channels": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3ddon/channels",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3ddon/conversations",
                            "teammates": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3ddon/teammates",
                            "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                        },
                    },
                    "id": "inb_3ddon",
                    "name": "Harley Staging",
                    "is_private": False,
                    "is_public": True,
                    "custom_fields": {},
                },
                {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3e07b",
                        "related": {
                            "channels": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3e07b/channels",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3e07b/conversations",
                            "teammates": "https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3e07b/teammates",
                            "owner": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                        },
                    },
                    "id": "inb_3e07b",
                    "name": "Production partner channel test",
                    "is_private": False,
                    "is_public": False,
                    "custom_fields": {},
                },
            ],
            "members": [
                {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7",
                        "related": {
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/inboxes",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_b2c7/conversations",
                        },
                    },
                    "id": "tea_b2c7",
                    "email": "amanie@meya.ai",
                    "username": "amanie",
                    "first_name": "Amanie",
                    "last_name": "Ismail",
                    "is_admin": True,
                    "is_available": True,
                    "is_blocked": False,
                    "custom_fields": {},
                },
                {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_d0t3",
                        "related": {
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_d0t3/inboxes",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_d0t3/conversations",
                        },
                    },
                    "id": "tea_d0t3",
                    "email": "harley+old@meya.ai",
                    "username": "harley",
                    "first_name": "",
                    "last_name": "",
                    "is_admin": False,
                    "is_available": False,
                    "is_blocked": True,
                    "custom_fields": {},
                },
                {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_d0tj",
                        "related": {
                            "inboxes": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_d0tj/inboxes",
                            "conversations": "https://meya-partner-developer-account.api.frontapp.com/teammates/tea_d0tj/conversations",
                        },
                    },
                    "id": "tea_d0tj",
                    "email": "support@meya.ai",
                    "username": "support",
                    "first_name": "Meya",
                    "last_name": "Bot",
                    "is_admin": True,
                    "is_available": True,
                    "is_blocked": False,
                    "custom_fields": {},
                },
            ],
        }
    ) == FrontTeam(
        id="tim_6xuv",
        name="Meya Partner Developer Account",
        inboxes=[
            FrontInbox(
                links=FrontInboxLinksRelated(
                    related=FrontInboxLinks(
                        channels="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_326dj/channels",
                        conversations="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_326dj/conversations",
                        teammates="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_326dj/teammates",
                        owner="https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                    )
                ),
                id="inb_326dj",
                name="Front + Meya [test]",
                is_private=False,
                is_public=False,
                custom_fields={},
            ),
            FrontInbox(
                links=FrontInboxLinksRelated(
                    related=FrontInboxLinks(
                        channels="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_368ef/channels",
                        conversations="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_368ef/conversations",
                        teammates="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_368ef/teammates",
                        owner="https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                    )
                ),
                id="inb_368ef",
                name="Seal Team 6",
                is_private=False,
                is_public=False,
                custom_fields={},
            ),
            FrontInbox(
                links=FrontInboxLinksRelated(
                    related=FrontInboxLinks(
                        channels="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_39ifb/channels",
                        conversations="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_39ifb/conversations",
                        teammates="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_39ifb/teammates",
                        owner="https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                    )
                ),
                id="inb_39ifb",
                name="Priority inbox",
                is_private=False,
                is_public=False,
                custom_fields={},
            ),
            FrontInbox(
                links=FrontInboxLinksRelated(
                    related=FrontInboxLinks(
                        channels="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_39ukn/channels",
                        conversations="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_39ukn/conversations",
                        teammates="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_39ukn/teammates",
                        owner="https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                    )
                ),
                id="inb_39ukn",
                name="Harley",
                is_private=False,
                is_public=False,
                custom_fields={},
            ),
            FrontInbox(
                links=FrontInboxLinksRelated(
                    related=FrontInboxLinks(
                        channels="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3c98n/channels",
                        conversations="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3c98n/conversations",
                        teammates="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3c98n/teammates",
                        owner="https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                    )
                ),
                id="inb_3c98n",
                name="Front Demo",
                is_private=False,
                is_public=False,
                custom_fields={},
            ),
            FrontInbox(
                links=FrontInboxLinksRelated(
                    related=FrontInboxLinks(
                        channels="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d3t3/channels",
                        conversations="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d3t3/conversations",
                        teammates="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d3t3/teammates",
                        owner="https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                    )
                ),
                id="inb_3d3t3",
                name="Channel Api",
                is_private=False,
                is_public=False,
                custom_fields={},
            ),
            FrontInbox(
                links=FrontInboxLinksRelated(
                    related=FrontInboxLinks(
                        channels="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d9vr/channels",
                        conversations="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d9vr/conversations",
                        teammates="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3d9vr/teammates",
                        owner="https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                    )
                ),
                id="inb_3d9vr",
                name="Disney",
                is_private=False,
                is_public=True,
                custom_fields={},
            ),
            FrontInbox(
                links=FrontInboxLinksRelated(
                    related=FrontInboxLinks(
                        channels="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3ddon/channels",
                        conversations="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3ddon/conversations",
                        teammates="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3ddon/teammates",
                        owner="https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                    )
                ),
                id="inb_3ddon",
                name="Harley Staging",
                is_private=False,
                is_public=True,
                custom_fields={},
            ),
            FrontInbox(
                links=FrontInboxLinksRelated(
                    related=FrontInboxLinks(
                        channels="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3e07b/channels",
                        conversations="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3e07b/conversations",
                        teammates="https://meya-partner-developer-account.api.frontapp.com/inboxes/inb_3e07b/teammates",
                        owner="https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv",
                    )
                ),
                id="inb_3e07b",
                name="Production partner channel test",
                is_private=False,
                is_public=False,
                custom_fields={},
            ),
        ],
        members=[
            FrontTeammateGet(
                id="tea_b2c7",
                email="amanie@meya.ai",
                username="amanie",
                first_name="Amanie",
                last_name="Ismail",
                is_admin=True,
                is_available=True,
                is_blocked=False,
                custom_fields={},
            ),
            FrontTeammateGet(
                id="tea_d0t3",
                email="harley+old@meya.ai",
                username="harley",
                first_name="",
                last_name="",
                is_admin=False,
                is_available=False,
                is_blocked=True,
                custom_fields={},
            ),
            FrontTeammateGet(
                id="tea_d0tj",
                email="support@meya.ai",
                username="support",
                first_name="Meya",
                last_name="Bot",
                is_admin=True,
                is_available=True,
                is_blocked=False,
                custom_fields={},
            ),
        ],
    )


def test_front_teams():
    assert FrontTeams.from_dict(
        {
            "_pagination": {"next": None},
            "_links": {
                "self": "https://meya-partner-developer-account.api.frontapp.com/teams/"
            },
            "_results": [
                {
                    "_links": {
                        "self": "https://meya-partner-developer-account.api.frontapp.com/teams/tim_6xuv"
                    },
                    "id": "tim_6xuv",
                    "name": "Meya Partner Developer Account",
                }
            ],
        }
    ) == FrontTeams(
        pagination=FrontPagination(next=None),
        results=[
            FrontTeamsData(
                id="tim_6xuv", name="Meya Partner Developer Account"
            )
        ],
    )
