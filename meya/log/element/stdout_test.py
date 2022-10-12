import pytest

from meya.component.entry.start import ComponentStartEntry
from meya.db.view.log import LogView
from meya.element.element_test import test_type_registry
from meya.element.element_test import verify_process_element
from meya.flow.entry.next import FlowNextEntry
from meya.log.element.stdout import StdoutLogElement
from meya.text.component.say import SayComponent
from meya.text.event.say import SayEvent

log = LogView()
log.info("Info message.")
log.error("Error message.")
log.debug("Debug message.")
log.exception()


@pytest.mark.parametrize(
    "sub_entry",
    [
        (log.entries[0]),
        (log.entries[1]),
        (log.entries[2]),
        (log.entries[3]),
        (
            ComponentStartEntry(
                bot_id="grid_bot",
                data={},
                flow="flow",
                index=0,
                spec=dict(
                    path=SayComponent.get_element_type(test_type_registry),
                    config=dict(text="hello, world"),
                ),
                stack=[],
                thread_id="T0",
            )
        ),
        (SayEvent(user_id="U123", text="hey there!", thread_id="T123")),
        (
            FlowNextEntry(
                bot_id="grid_bot",
                data={},
                flow="flow",
                index=1,
                stack=[],
                thread_id="T0",
            )
        ),
    ],
)
@pytest.mark.asyncio
async def test_log(sub_entry):
    log_element = StdoutLogElement()
    await verify_process_element(
        element=log_element, sub_entry=sub_entry, expected_pub_entries=[]
    )
