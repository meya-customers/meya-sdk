from meya.zendesk.support.payload.ticket import ZendeskSupportTicketGet
from meya.zendesk.support.payload.ticket import ZendeskSupportTicketStatus
from meya.zendesk.support.payload.ticket_field import (
    ZendeskSupportTicketFieldPair,
)


def test_ticket_get_from_dict():
    assert ZendeskSupportTicketGet.from_dict(
        {
            "id": 1519,
            "url": "https://d3v-meya.zendesk.com/api/v2/tickets/1519.json",
            "via": {
                "source": {"to": {}, "rel": None, "from": {}},
                "channel": "api",
            },
            "tags": [],
            "type": None,
            "due_at": None,
            "fields": [{"id": 360027800093, "value": None}],
            "status": "new",
            "subject": "SUBJECT",
            "brand_id": 114094100894,
            "group_id": None,
            "priority": None,
            "is_public": True,
            "recipient": None,
            "created_at": "2020-07-15T19:32:50Z",
            "problem_id": None,
            "updated_at": "2020-07-15T19:32:50Z",
            "assignee_id": None,
            "description": "BODY",
            "external_id": "t-85de2e21ea6f45d2ba0acef995c00f46",
            "raw_subject": "SUBJECT",
            "email_cc_ids": [],
            "follower_ids": [],
            "followup_ids": [],
            "requester_id": 416025657633,
            "submitter_id": 416025657633,
            "custom_fields": [
                {"id": 360027800093, "value": "Mac"},
                {"id": 360046919733, "value": "39.111"},
                {"id": 360046940234, "value": "9"},
                {"id": 360046924413, "value": ["logging", "storage"]},
                {"id": 360046919873, "value": True},
                {"id": 9999, "value": None},
            ],
            "has_incidents": False,
            "forum_topic_id": None,
            "ticket_form_id": 114093961313,
            "organization_id": None,
            "collaborator_ids": [],
            "allow_attachments": True,
            "allow_channelback": False,
            "satisfaction_rating": None,
            "sharing_agreement_ids": [],
            "satisfaction_probability": None,
            "comment_count": 9,
        }
    ) == ZendeskSupportTicketGet(
        comment_count=9,
        created_at="2020-07-15T19:32:50Z",
        custom_fields=[
            ZendeskSupportTicketFieldPair(id=360027800093, value="Mac"),
            ZendeskSupportTicketFieldPair(id=360046919733, value="39.111"),
            ZendeskSupportTicketFieldPair(id=360046940234, value="9"),
            ZendeskSupportTicketFieldPair(
                id=360046924413, value=["logging", "storage"]
            ),
            ZendeskSupportTicketFieldPair(id=360046919873, value=True),
            ZendeskSupportTicketFieldPair(id=9999, value=None),
        ],
        description="BODY",
        external_id="t-85de2e21ea6f45d2ba0acef995c00f46",
        id=1519,
        requester_id=416025657633,
        status=ZendeskSupportTicketStatus.NEW,
        subject="SUBJECT",
        updated_at="2020-07-15T19:32:50Z",
        ticket_form_id=114093961313,
        brand_id=114094100894,
    )
