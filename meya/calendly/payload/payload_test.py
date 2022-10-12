import copy
import pytest

from meya.calendly.event import CalendlyEvent
from meya.calendly.payload.payload import CalendlyEventType
from meya.calendly.payload.payload import CalendlyEventV2
from meya.calendly.payload.payload import CalendlyGetEventResponse
from meya.calendly.payload.payload import CalendlyWebhook
from meya.util import json
from meya.util.dict import from_dict
from typing import Any
from typing import Dict
from typing import Optional

INVITEE_CREATED_PAYLOAD: dict = json.from_json(
    """
{
  "event":"invitee.created",
  "time":"2018-03-14T19:16:01Z",
  "payload":{
    "event_type":{  
      "uuid":"CCCCCCCCCCCCCCCC",
      "kind":"One-on-One",
      "slug":"event_type_name",
      "name":"Event Type Name",
      "duration":15,
      "owner":{  
        "type":"users",
        "uuid":"DDDDDDDDDDDDDDDD"
      }
    },
    "event":{  
      "uuid":"BBBBBBBBBBBBBBBB",
      "assigned_to":[  
        "Jane Sample Data"
      ],
      "extended_assigned_to":[  
        {  
          "name":"Jane Sample Data",
          "email":"user@example.com",
          "primary":false
        }
      ],
      "start_time":"2018-03-14T12:00:00Z",
      "start_time_pretty":"12:00pm - Wednesday, March 14, 2018",
      "invitee_start_time":"2018-03-14T12:00:00Z",
      "invitee_start_time_pretty":"12:00pm - Wednesday, March 14, 2018",
      "end_time":"2018-03-14T12:15:00Z",
      "end_time_pretty":"12:15pm - Wednesday, March 14, 2018",
      "invitee_end_time":"2018-03-14T12:15:00Z",
      "invitee_end_time_pretty":"12:15pm - Wednesday, March 14, 2018",
      "created_at":"2018-03-14T00:00:00Z",
      "location":"The Coffee Shop",
      "canceled":false,
      "canceler_name":null,
      "cancel_reason":null,
      "canceled_at":null
    },
    "invitee":{  
      "uuid":"AAAAAAAAAAAAAAAA",
      "first_name":"Joe",
      "last_name":"Sample Data",
      "name":"Joe Sample Data",
      "email":"not.a.real.email@example.com",
      "text_reminder_number":"+14045551234",
      "timezone":"UTC",
      "created_at":"2018-03-14T00:00:00Z",
      "is_reschedule":false,
      "payments":[  
        {  
          "id":"ch_AAAAAAAAAAAAAAAAAAAAAAAA",
          "provider":"stripe",
          "amount":1234.56,
          "currency":"USD",
          "terms":"sample terms of payment (up to 1,024 characters)",
          "successful":true
        }
      ],
      "canceled":false,
      "canceler_name":null,
      "cancel_reason":null,
      "canceled_at":null
    },
    "questions_and_answers":[  
      {  
        "question":"Skype ID",
        "answer":"fake_skype_id"
      },
      {  
        "question":"Facebook ID",
        "answer":"fake_facebook_id"
      },
      {  
        "question":"Twitter ID",
        "answer":"fake_twitter_id"
      },
      {  
        "question":"Google ID",
        "answer":"fake_google_id"
      }
    ],
    "questions_and_responses":{  
      "1_question":"Skype ID",
      "1_response":"fake_skype_id",
      "2_question":"Facebook ID",
      "2_response":"fake_facebook_id",
      "3_question":"Twitter ID",
      "3_response":"fake_twitter_id",
      "4_question":"Google ID",
      "4_response":"fake_google_id"
    },
    "tracking":{  
      "utm_campaign":null,
      "utm_source":"meya",
      "utm_medium":null,
      "utm_content": "thread_id_here:user_id_here:booking_id_here",
      "utm_term":null,
      "salesforce_uuid":null
    },
    "old_event":null,
    "old_invitee":null,
    "new_event":null,
    "new_invitee":null
  }
}
"""
)
INVITEE_CANCELED_PAYLOAD: dict = json.from_json(
    """
{
  "event":"invitee.canceled",
  "time":"2018-03-14T19:16:01Z",
  "payload":{
    "event_type":{
      "uuid":"CCCCCCCCCCCCCCCC",
      "kind":"One-on-One",
      "slug":"event_type_name",
      "name":"Event Type Name",
      "duration":15,
      "owner":{
        "type":"users",
        "uuid":"DDDDDDDDDDDDDDDD"
      }
    },
    "event":{
      "uuid":"BBBBBBBBBBBBBBBB",
      "assigned_to":[
        "Jane Sample Data"
      ],
      "extended_assigned_to":[
        {
          "name":"Jane Sample Data",
          "email":"user@example.com",
          "primary":false
        }
      ],
      "start_time":"2018-03-14T12:00:00Z",
      "start_time_pretty":"12:00pm - Wednesday, March 14, 2018",
      "invitee_start_time":"2018-03-14T12:00:00Z",
      "invitee_start_time_pretty":"12:00pm - Wednesday, March 14, 2018",
      "end_time":"2018-03-14T12:15:00Z",
      "end_time_pretty":"12:15pm - Wednesday, March 14, 2018",
      "invitee_end_time":"2018-03-14T12:15:00Z",
      "invitee_end_time_pretty":"12:15pm - Wednesday, March 14, 2018",
      "created_at":"2018-03-14T00:00:00Z",
      "location":"The Coffee Shop",
      "canceled":true,
      "canceler_name":"Joe Sample Data",
      "cancel_reason":"This was not a real meeting.",
      "canceled_at":"2018-03-14T00:00:00Z"
    },
    "invitee":{
      "uuid":"AAAAAAAAAAAAAAAA",
      "first_name":"Joe",
      "last_name":"Sample Data",
      "name":"Joe Sample Data",
      "email":"not.a.real.email@example.com",
      "text_reminder_number":"+14045551234",
      "timezone":"UTC",
      "created_at":"2018-03-14T00:00:00Z",
      "is_reschedule":false,
      "payments":[
        {
          "id":"ch_AAAAAAAAAAAAAAAAAAAAAAAA",
          "provider":"stripe",
          "amount":1234.56,
          "currency":"USD",
          "terms":"sample terms of payment (up to 1,024 characters)",
          "successful":true
        }
      ],
      "canceled":true,
      "canceler_name":"Joe Sample Data",
      "cancel_reason":"This was not a real meeting.",
      "canceled_at":"2018-03-14T00:00:00Z"
    },
    "questions_and_answers":[
      {
        "question":"Skype ID",
        "answer":"fake_skype_id"
      },
      {
        "question":"Facebook ID",
        "answer":"fake_facebook_id"
      },
      {
        "question":"Twitter ID",
        "answer":"fake_twitter_id"
      },
      {
        "question":"Google ID",
        "answer":"fake_google_id"
      }
    ],
    "questions_and_responses":{
      "1_question":"Skype ID",
      "1_response":"fake_skype_id",
      "2_question":"Facebook ID",
      "2_response":"fake_facebook_id",
      "3_question":"Twitter ID",
      "3_response":"fake_twitter_id",
      "4_question":"Google ID",
      "4_response":"fake_google_id"
    },
    "tracking":{
      "utm_campaign":null,
      "utm_source":"meya",
      "utm_medium":null,
      "utm_content": "thread_id_here:user_id_here:booking_id_here",
      "utm_term":null,
      "salesforce_uuid":null
    },
    "old_event":null,
    "old_invitee":null,
    "new_event":null,
    "new_invitee":null
  }
}
"""
)
SAMPLED_INVITEE_CREATED: dict = json.from_json(
    """
{
    "event": "invitee.created",
    "time": "2018-03-14T19:16:01Z",
    "payload": {
        "event_type": {
            "uuid": "HEDPHY7NS2P3IU2S",
            "kind": "One-on-One",
            "slug": "meya-demo",
            "name": "Meya Demo",
            "duration": 15,
            "owner": {
                "type": "users",
                "uuid": "AEAAGFG2EVL3JM2H"
            }
        },
        "event": {
            "uuid": "DHPESBXW5MONHVC7",
            "assigned_to": [
                "Erik Kalviainen"
            ],
            "extended_assigned_to": [
                {
                    "name": "Erik Kalviainen",
                    "email": "erik@meya.ai",
                    "primary": true
                }
            ],
            "start_time": "2019-10-09T09:30:00-04:00",
            "start_time_pretty": "09:30am - Wednesday, October 9, 2019",
            "invitee_start_time": "2019-10-09T09:30:00-04:00",
            "invitee_start_time_pretty": "09:30am - Wednesday, October 9, 2019",
            "end_time": "2019-10-09T09:45:00-04:00",
            "end_time_pretty": "09:45am - Wednesday, October 9, 2019",
            "invitee_end_time": "2019-10-09T09:45:00-04:00",
            "invitee_end_time_pretty": "09:45am - Wednesday, October 9, 2019",
            "created_at": "2019-10-08T16:15:51-04:00",
            "location": null,
            "canceled": false,
            "canceler_name": null,
            "cancel_reason": null,
            "canceled_at": null
        },
        "invitee": {
            "uuid": "CAKC4VS3EYZXAISR",
            "first_name": null,
            "last_name": null,
            "name": "Erik",
            "email": "erik+test@meya.ai",
            "text_reminder_number": null,
            "timezone": "America/New_York",
            "created_at": "2019-10-08T16:15:51-04:00",
            "is_reschedule": false,
            "payments": [],
            "canceled": false,
            "canceler_name": null,
            "cancel_reason": null,
            "canceled_at": null
        },
        "questions_and_answers": [],
        "questions_and_responses": {},
        "tracking": {
            "utm_campaign": null,
            "utm_source": "meya",
            "utm_medium": null,
            "utm_content": "thread_id_here:user_id_here:booking_id_here",
            "utm_term": null,
            "salesforce_uuid": null
        },
        "old_event": null,
        "old_invitee": null,
        "new_event": null,
        "new_invitee": null
    }
}
"""
)
ROGUE_INVITEE_CREATED = copy.deepcopy(SAMPLED_INVITEE_CREATED)
ROGUE_INVITEE_CREATED["payload"]["tracking"] = {
    "utm_campaign": None,
    "utm_source": None,
    "utm_medium": None,
    "utm_content": None,
    "utm_term": None,
    "salesforce_uuid": None,
}
STATIC_INVITEE_CREATED = copy.deepcopy(SAMPLED_INVITEE_CREATED)
STATIC_INVITEE_CREATED["payload"]["tracking"] = {
    "utm_campaign": None,
    "utm_source": "meya",
    "utm_medium": None,
    "utm_content": "thread_id_here:user_id_here",
    "utm_term": None,
    "salesforce_uuid": None,
}
ROGUE_EVENT_TYPE = copy.deepcopy(SAMPLED_INVITEE_CREATED)
ROGUE_EVENT_TYPE["event"] = "RANDOM_EVENT_123"


@pytest.mark.parametrize(
    (
        "payload_dict",
        "event_type",
        "thread_id",
        "user_id",
        "booking_id",
        "valid_payload",
        "valid_event",
    ),
    [
        (
            INVITEE_CREATED_PAYLOAD,
            CalendlyEventType.INVITEE_CREATED,
            "thread_id_here",
            "user_id_here",
            "booking_id_here",
            True,
            True,
        ),
        (
            INVITEE_CANCELED_PAYLOAD,
            CalendlyEventType.INVITEE_CANCELED,
            "thread_id_here",
            "user_id_here",
            "booking_id_here",
            True,
            True,
        ),
        ({}, None, None, None, None, False, False),
        (
            ROGUE_INVITEE_CREATED,
            CalendlyEventType.INVITEE_CREATED,
            None,
            None,
            None,
            True,
            False,
        ),
        (
            STATIC_INVITEE_CREATED,
            CalendlyEventType.INVITEE_CREATED,
            "thread_id_here",
            "user_id_here",
            None,
            True,
            True,
        ),
        (ROGUE_EVENT_TYPE, None, None, None, None, False, False),
    ],
)
@pytest.mark.asyncio
async def test_calendly_models(
    payload_dict: Dict[str, Any],
    event_type: Optional[CalendlyEventType],
    thread_id: Optional[str],
    user_id: Optional[str],
    booking_id: Optional[str],
    valid_payload: bool,
    valid_event: bool,
):
    # attempt to load the webhook model from the raw payload dict
    try:
        webhook = from_dict(CalendlyWebhook, payload_dict)
    except ValueError:
        webhook = None
    if valid_payload:
        assert isinstance(webhook, CalendlyWebhook)
    else:
        return

    # if it's a valid payload, let's test some more
    assert webhook.event == event_type
    assert webhook.thread_id == thread_id
    assert webhook.user_id == user_id
    assert webhook.booking_id == booking_id
    if valid_event:
        assert isinstance(webhook.to_event(), CalendlyEvent)
    else:
        assert webhook.to_event() is None
    assert webhook.time == "2018-03-14T19:16:01Z"


@pytest.mark.parametrize(
    ("utm_content", "part_0", "part_1", "part_2"),
    [
        ("foo:bar", "foo", "bar", None),
        ("foo", None, None, None),
        (None, None, None, None),
        ("foo:bar:fizz", "foo", "bar", "fizz"),
        ("foo:", "foo", "", None),
        (":bar", "", "bar", None),
        ("foo:bar:", "foo", "bar", ""),
        (":", "", "", None),
        ("::", "", "", ""),
    ],
)
def test_encode_decode_utm_content(
    utm_content: str,
    part_0: Optional[str],
    part_1: Optional[str],
    part_2: Optional[str],
):
    assert CalendlyWebhook.decode_utm_content(utm_content) == (
        part_0,
        part_1,
        part_2,
    )
    if part_0 is not None and part_1 is not None:
        assert (
            CalendlyWebhook.encode_utm_content(part_0, part_1, part_2)
            == utm_content
        )


def test_get_event_response():
    assert from_dict(
        CalendlyGetEventResponse,
        {
            "resource": {
                "created_at": "2022-01-25T16:41:11.642294Z",
                "end_time": "2022-01-27T14:30:00.000000Z",
                "event_guests": [],
                "event_memberships": [
                    {"user": "https://api.calendly.com/users/DGECLAZIYZVXO5VX"}
                ],
                "event_type": "https://api.calendly.com/event_types/BDAOW4AMU5HCSH7O",
                "invitees_counter": {"active": 1, "limit": 1, "total": 1},
                "location": {
                    "data": {
                        "id": 83594658585,
                        "settings": {
                            "global_dial_in_numbers": [
                                {
                                    "country_name": "US",
                                    "city": "Washington DC",
                                    "number": "+1 3017158592",
                                    "type": "toll",
                                    "country": "US",
                                },
                                {
                                    "country_name": "US",
                                    "city": "Chicago",
                                    "number": "+1 3126266799",
                                    "type": "toll",
                                    "country": "US",
                                },
                                {
                                    "country_name": "US",
                                    "city": "New York",
                                    "number": "+1 6465588656",
                                    "type": "toll",
                                    "country": "US",
                                },
                                {
                                    "country_name": "US",
                                    "city": "Tacoma",
                                    "number": "+1 2532158782",
                                    "type": "toll",
                                    "country": "US",
                                },
                                {
                                    "country_name": "US",
                                    "city": "Houston",
                                    "number": "+1 3462487799",
                                    "type": "toll",
                                    "country": "US",
                                },
                                {
                                    "country_name": "US",
                                    "city": "San Jose",
                                    "number": "+1 6699006833",
                                    "type": "toll",
                                    "country": "US",
                                },
                            ]
                        },
                        "extra": {
                            "intl_numbers_url": "https://us02web.zoom.us/u/kcaqNMiDPX"
                        },
                        "password": "107978",
                    },
                    "join_url": "https://us02web.zoom.us/j/83594658585?pwd=dUk5ZEpoWEE1Ni8zZ0NTcW42Z0w3dz09",
                    "status": "pushed",
                    "type": "zoom",
                },
                "name": "30 Minute Meeting",
                "start_time": "2022-01-27T14:00:00.000000Z",
                "status": "active",
                "updated_at": "2022-01-25T16:41:11.642294Z",
                "uri": "https://api.calendly.com/scheduled_events/8e87d9c9-2c85-45d6-af2d-41a77e6d51b2",
            }
        },
    ) == CalendlyGetEventResponse(
        resource=CalendlyEventV2(
            uri="https://api.calendly.com/scheduled_events/8e87d9c9-2c85-45d6-af2d-41a77e6d51b2",
            name="30 Minute Meeting",
            status="active",
            start_time="2022-01-27T14:00:00.000000Z",
            end_time="2022-01-27T14:30:00.000000Z",
            event_type="https://api.calendly.com/event_types/BDAOW4AMU5HCSH7O",
            location={
                "data": {
                    "id": 83594658585,
                    "settings": {
                        "global_dial_in_numbers": [
                            {
                                "country_name": "US",
                                "city": "Washington DC",
                                "number": "+1 3017158592",
                                "type": "toll",
                                "country": "US",
                            },
                            {
                                "country_name": "US",
                                "city": "Chicago",
                                "number": "+1 3126266799",
                                "type": "toll",
                                "country": "US",
                            },
                            {
                                "country_name": "US",
                                "city": "New York",
                                "number": "+1 6465588656",
                                "type": "toll",
                                "country": "US",
                            },
                            {
                                "country_name": "US",
                                "city": "Tacoma",
                                "number": "+1 2532158782",
                                "type": "toll",
                                "country": "US",
                            },
                            {
                                "country_name": "US",
                                "city": "Houston",
                                "number": "+1 3462487799",
                                "type": "toll",
                                "country": "US",
                            },
                            {
                                "country_name": "US",
                                "city": "San Jose",
                                "number": "+1 6699006833",
                                "type": "toll",
                                "country": "US",
                            },
                        ]
                    },
                    "extra": {
                        "intl_numbers_url": "https://us02web.zoom.us/u/kcaqNMiDPX"
                    },
                    "password": "107978",
                },
                "join_url": "https://us02web.zoom.us/j/83594658585?pwd=dUk5ZEpoWEE1Ni8zZ0NTcW42Z0w3dz09",
                "status": "pushed",
                "type": "zoom",
            },
            invitees_counter={"active": 1, "limit": 1, "total": 1},
            created_at="2022-01-25T16:41:11.642294Z",
            updated_at="2022-01-25T16:41:11.642294Z",
            event_memberships=[
                {"user": "https://api.calendly.com/users/DGECLAZIYZVXO5VX"}
            ],
            event_guests=[],
        )
    )
