import pytest

from meya.element.element_test import create_flow_start_entry
from meya.element.element_test import create_say_event
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import verify_trigger_match
from meya.text.trigger.regex import RegexTrigger
from meya.text.trigger.regex import RegexTriggerResponse
from meya.trigger.element import Trigger
from meya.util.dict import to_dict


@pytest.mark.asyncio
@pytest.mark.parametrize(
    (
        "text",
        "regex",
        "ignorecase",
        "confidence",
        "should_match",
        "result",
        "groups",
    ),
    [
        ("random_text_here", ".*", None, None, True, "random_text_here", {}),
        ("This is a WORD, yo!", r"\bword\b", None, None, True, "WORD", {}),
        ("This is a WORD, yo!", r"\b word \b", True, None, True, "WORD", {}),
        ("This is a WORD, yo!", r"\bword\b", False, None, False, None, None),
        ("This is aWORDyo!", r"\bword\b", None, None, False, None, None),
        (
            "IMG12.png",
            r"^(IMG\d+\.(?P<ext>png))$",
            None,
            None,
            True,
            "IMG12.png",
            {0: "IMG12.png", 1: "png", "ext": "png"},
        ),
        (
            "This is aWORDyo!",
            r"\bword\b",
            None,
            Trigger.MAX_CONFIDENCE,
            True,
            "",
            {},
        ),
        (
            "/path/to/riches/1000000000",
            r"^(/path/to/(?P<key>.*)/(?P<value>.*))$",
            None,
            Trigger.MAX_CONFIDENCE,
            True,
            "/path/to/riches/1000000000",
            {
                0: "/path/to/riches/1000000000",
                1: "riches",
                2: "1000000000",
                "key": "riches",
                "value": "1000000000",
            },
        ),
    ],
)
async def test_trigger(
    text, regex, ignorecase, confidence, should_match, result, groups
):
    event = create_say_event(text)
    trigger = RegexTrigger(
        regex=regex,
        ignorecase=ignorecase,
        action=create_trigger_action_entry(
            create_flow_start_entry(event.thread_id)
        ),
        confidence=confidence,
    )
    match_data = to_dict(RegexTriggerResponse(result=result, groups=groups))
    await verify_trigger_match(
        trigger,
        event,
        should_match=should_match,
        confidence=confidence,
        match_data=match_data,
    )
