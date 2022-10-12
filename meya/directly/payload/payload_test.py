import pytest

from meya.directly.payload.payload import DirectlyWebhookPayload
from meya.directly.payload.payload import EventType
from meya.http.payload import PayloadError
from typing import Any
from typing import Dict
from typing import Optional


def test_create_schema():
    schema = DirectlyWebhookPayload.dump_schema()
    assert (
        schema
        == """{
 "event_type": "{{event_type}}",
 "timestamp": {{timestamp.time_ms}},
 "question": {
  "uuid": "{{question.uuid}}",
  "timestamp": {{question.date_created.time_ms}},
  "subject": "{{question.subject}}",
  "text": "{{question.text}}"
 },
 "answer": {
  "uuid": "{{answer.uuid}}",
  "timestamp": {{answer.date_created.time_ms}},
  "text": "{{answer.text}}",
  "author": {
   "uuid": "{{answer.author.uuid}}",
   "name": "{{answer.author.name}}",
   "avatar": "{{answer.author.avatar}}"
  },
  "expert": {
   "uuid": "{{answer.expert.uuid}}",
   "name": "{{answer.expert.name}}",
   "avatar": "{{answer.expert.avatar}}"
  },
  "comment": {
   "uuid": "{{answer.comment.uuid}}",
   "timestamp": {{answer.comment.date_created.time_ms}},
   "text": "{{answer.comment.text}}",
   "is_auto_answer": {{answer.comment.is_auto_answer}},
   "author": {
    "uuid": "{{answer.comment.author.uuid}}",
    "name": "{{answer.comment.author.name}}",
    "avatar": "{{answer.comment.author.avatar}}",
    "is_poster": {{answer.comment.author.is_poster}},
    "is_chatbot": {{answer.comment.author.is_chatbot}}
   }
  }
 },
 "message": {
  "uuid": "{{message.uuid}}",
  "text": "{{message.text}}"
 },
 "extra": {{extra}}
}"""
    )


QUESTION = {
    "text": "When will the bots take over? [248]",
    "uuid": "87322703-c798-4312-82d9-00a32d94b405",
    "subject": "Bots [248]",
    "timestamp": 1584632329000,
}
ANSWER = {
    "text": "123456789",
    "uuid": "ccd55139-1bc6-476d-ac88-a6c66741af4d",
    "author": {
        "name": "Erik K.",
        "uuid": "d06b413f-99f0-4aa8-917b-0addd1b8300a",
        "avatar": "https://directly-static.s3.amazonaws.com/avatars/250x250/16248363.jpg?AWSAccessKeyId=AKIAIDWNCANEJGMPSSOA&Expires=1585929857&Signature=PwCA%2FeokCsUOqufiXMEzvYKdNvE%3D",
    },
    "expert": {
        "name": "Erik K.",
        "uuid": "d06b413f-99f0-4aa8-917b-0addd1b8300a",
        "avatar": "https://directly-static.s3.amazonaws.com/avatars/250x250/16248363.jpg?AWSAccessKeyId=AKIAIDWNCANEJGMPSSOA&Expires=1585929857&Signature=PwCA%2FeokCsUOqufiXMEzvYKdNvE%3D",
    },
    "comment": {
        "text": "123456789",
        "uuid": "36be2662-cf2c-4ba8-8273-bfcc9f12af98",
        "author": {
            "name": "Erik K.",
            "uuid": "d06b413f-99f0-4aa8-917b-0addd1b8300a",
            "avatar": "https://directly-static.s3.amazonaws.com/avatars/250x250/16248363.jpg?AWSAccessKeyId=AKIAIDWNCANEJGMPSSOA&Expires=1585929857&Signature=PwCA%2FeokCsUOqufiXMEzvYKdNvE%3D",
            "is_poster": False,
            "is_chatbot": False,
            "is_auto_answer": False,
        },
        "timestamp": 1584633857000,
    },
    "timestamp": 1584633857000,
}
MESSAGE = {"text": "123456789", "uuid": "ccd55139-1bc6-476d-ac88-a6c66741af4d"}
QUESTION_APPROVED = {
    "question": QUESTION,
    "timestamp": 1584632329662,
    "event_type": "QUESTION_APPROVED",
}
QUESTION_CLAIMED = {
    "question": QUESTION,
    "timestamp": 1584633706807,
    "event_type": "QUESTION_CLAIMED",
}
QUESTION_RESPONSE = {
    "answer": ANSWER,
    "question": QUESTION,
    "timestamp": 1584633856985,
    "event_type": "QUESTION_RESPONSE",
}
QUESTION_MARKED_AS_RESOLVED = {
    "question": QUESTION,
    "timestamp": 1584633706807,
    "event_type": "QUESTION_MARKED_AS_RESOLVED",
    "message": MESSAGE,
}
QUESTION_FLAGGED_EMERGENCY = {
    "question": QUESTION,
    "timestamp": 1584633706807,
    "event_type": "QUESTION_FLAGGED_EMERGENCY",
}
QUESTION_FLAGGED_PII = {
    "question": QUESTION,
    "timestamp": 1584633706807,
    "event_type": "QUESTION_FLAGGED_PII",
}
QUESTION_REJECTED_BY_KEYWORD = {
    "question": QUESTION,
    "timestamp": 1584633706807,
    "event_type": "QUESTION_REJECTED_BY_KEYWORD",
}


@pytest.mark.parametrize(
    (
        "payload_dict",
        "valid",
        "event_type",
        "has_question",
        "has_answer",
        "has_message",
    ),
    [
        (
            {"event_type": "UNKNOWN_EVENT_TYPE", "timestamp": 1584632329662},
            False,
            None,
            False,
            False,
            False,
        ),
        (
            QUESTION_APPROVED,
            True,
            EventType.QUESTION_APPROVED,
            True,
            False,
            False,
        ),
        (
            {**QUESTION_APPROVED, **{"extra": {"foo": "bar"}}},
            True,
            EventType.QUESTION_APPROVED,
            True,
            False,
            False,
        ),
        (
            QUESTION_CLAIMED,
            True,
            EventType.QUESTION_CLAIMED,
            True,
            False,
            False,
        ),
        (
            QUESTION_RESPONSE,
            True,
            EventType.QUESTION_RESPONSE,
            True,
            True,
            False,
        ),
        (
            QUESTION_MARKED_AS_RESOLVED,
            True,
            EventType.QUESTION_MARKED_AS_RESOLVED,
            True,
            False,
            True,
        ),
        (
            QUESTION_FLAGGED_EMERGENCY,
            True,
            EventType.QUESTION_FLAGGED_EMERGENCY,
            True,
            False,
            False,
        ),
        (
            QUESTION_FLAGGED_PII,
            True,
            EventType.QUESTION_FLAGGED_PII,
            True,
            False,
            False,
        ),
        (
            QUESTION_REJECTED_BY_KEYWORD,
            True,
            EventType.QUESTION_REJECTED_BY_KEYWORD,
            True,
            False,
            False,
        ),
    ],
)
def test_event_deserialize(
    payload_dict: Dict[str, Any],
    valid: bool,
    event_type: Optional[str],
    has_question: bool,
    has_answer: bool,
    has_message: bool,
):
    try:
        event = DirectlyWebhookPayload.from_dict(payload_dict)
    except PayloadError:
        event = None
    except:
        raise
    if not valid:
        return

    assert event is not None
    assert event.event_type == event_type
    assert event.timestamp > 1000
    if has_question:
        assert event.question
    else:
        assert event.question is None
    if has_answer:
        assert event.answer
    else:
        assert event.answer is None
    if has_message:
        assert event.message
    else:
        assert event.message is None
