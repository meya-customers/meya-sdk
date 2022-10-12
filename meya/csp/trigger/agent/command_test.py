import pytest

from meya.csp.event.agent.command import AgentCommandEvent
from meya.csp.trigger.agent.command import AgentCommandTrigger
from meya.db.view.user import UserType
from meya.element.element_test import create_flow_start_entry
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import create_user
from meya.element.element_test import verify_trigger_match
from meya.text.trigger.regex import RegexTrigger


@pytest.mark.parametrize(
    ("text", "regex", "ignorecase", "should_match", "result", "groups"),
    [
        ("/slashcommand", ".*", None, True, "/slashcommand", {}),
        ("/slashcommand", r"\bfoobar\b", False, False, None, None),
        (
            "/approve.leave",
            r"^(/approve\.(?P<form>leave))$",
            None,
            True,
            "/approve.leave",
            {0: "/approve.leave", 1: "leave", "form": "leave"},
        ),
    ],
)
@pytest.mark.asyncio
async def test_trigger(text, regex, ignorecase, should_match, result, groups):
    event_user = create_user(data=dict(type=UserType.AGENT))
    event = AgentCommandEvent(
        text=text, thread_id="t-0", user_id=event_user.id
    )
    trigger = AgentCommandTrigger(
        action=create_trigger_action_entry(
            create_flow_start_entry(event.thread_id)
        ),
        agent_command=regex,
        ignorecase=ignorecase,
    )
    match_data = {
        RegexTrigger.RESULT_KEY: result,
        RegexTrigger.GROUPS_KEY: groups,
    }
    await verify_trigger_match(
        trigger,
        event,
        should_match=should_match,
        match_data=match_data,
        event_user=event_user,
    )
