import pytest

from meya.component.element import ComponentErrorResponse
from meya.element.element_test import activate_triggers
from meya.element.element_test import create_component_next_entry
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import verify_process_element
from meya.event.composer_spec import ComposerEventSpec
from meya.event.composer_spec import ComposerFocus
from meya.event.composer_spec import ComposerVisibility
from meya.text.component.ask_regex import AskRegexComponent
from meya.text.component.ask_regex.ask_regex import (
    AskRegexComposerComponentOkResponse,
)
from meya.text.event.ask import AskEvent
from meya.text.trigger.regex import RegexTrigger
from meya.text.trigger.regex import RegexTriggerResponse
from meya.util.dict import to_dict

TEST_REGEX = r"""
    ^
    (?P<postal_first> [A-Za-z] \d [A-Za-z] )
    [ -]?
    (?P<postal_second> \d [A-Za-z] \d )
    $
"""


@pytest.mark.asyncio
async def test_component_next_valid():
    component = AskRegexComponent(
        ask="What is your postal code?", regex=TEST_REGEX
    )
    match_result = "A3A 4L7"
    match_groups = {
        0: "A3A",
        1: "4L7",
        "postal_first": "A3A",
        "postal_second": "4L7",
    }
    component_next_entry = create_component_next_entry(
        create_component_start_entry(component),
        data=to_dict(
            RegexTriggerResponse(result=match_result, groups=match_groups)
        ),
    )
    flow_next_entry = create_flow_next_entry(
        component_next_entry,
        data=to_dict(
            AskRegexComposerComponentOkResponse(
                result=match_result, groups=match_groups
            )
        ),
    )
    await verify_process_element(
        element=component,
        sub_entry=component_next_entry,
        expected_pub_entries=[flow_next_entry],
    )


@pytest.mark.asyncio
async def test_component_next_invalid_retry():
    component = AskRegexComponent(
        ask="What is your postal code?",
        regex=TEST_REGEX,
        error_message="Invalid postal code, please try again.",
    )
    component_next_entry = create_component_next_entry(
        create_component_start_entry(component),
        data=to_dict(RegexTriggerResponse(result="", groups={})),
    )
    ask_event = AskEvent(
        composer=ComposerEventSpec(
            focus=ComposerFocus.TEXT, visibility=ComposerVisibility.SHOW
        ),
        text=component.error_message,
    )
    triggers = activate_triggers(
        component_next_entry,
        RegexTrigger(
            regex=component.regex,
            ignorecase=component.ignorecase,
            confidence=component.confidence,
            action=create_trigger_action_entry(
                create_component_next_entry(
                    component_next_entry,
                    data=to_dict(
                        ComponentErrorResponse(result="", retry_count=1)
                    ),
                )
            ),
        ),
    )
    await verify_process_element(
        element=component,
        sub_entry=component_next_entry,
        expected_pub_entries=[ask_event, *triggers],
    )


@pytest.mark.asyncio
async def test_component_next_invalid_error():
    component = AskRegexComponent(
        ask="What is your postal code?", regex=TEST_REGEX, retries=1
    )
    component_next_entry = create_component_next_entry(
        create_component_start_entry(component),
        data={
            **to_dict(ComponentErrorResponse(result="", retry_count=1)),
            **to_dict(RegexTriggerResponse(result="", groups={})),
        },
    )
    flow_next_entry = create_flow_next_entry(component_next_entry)
    await verify_process_element(
        element=component,
        sub_entry=component_next_entry,
        expected_pub_entries=[flow_next_entry],
    )
