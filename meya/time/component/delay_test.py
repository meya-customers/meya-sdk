import pytest

from meya.element.element_error import ElementValidationError
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_thread
from meya.element.element_test import verify_process_element
from meya.text.event.say import SayEvent
from meya.time.component.delay import DelayComponent
from unittest.mock import AsyncMock
from unittest.mock import patch


def test_delay_validate_ok():
    component = DelayComponent(delay=1)
    component.validate()


def test_delay_validate_error():
    component = DelayComponent(delay=100)
    with pytest.raises(ElementValidationError) as excinfo:
        component.validate()
    assert str(excinfo.value) == "delay cannot be longer than 20 seconds"


@pytest.mark.asyncio
async def test_delay_component():
    delay = 5
    component = DelayComponent(delay=delay)
    component_start_entry = create_component_start_entry(component)
    flow_next_entry = create_flow_next_entry(component_start_entry)
    with patch(
        "meya.time.component.delay.asyncio.sleep", new_callable=AsyncMock
    ) as sleep_mock:
        await verify_process_element(
            element=component,
            sub_entry=component_start_entry,
            expected_pub_entries=[flow_next_entry],
        )
    sleep_mock.assert_called_with(delay)


@pytest.mark.asyncio
async def test_delay_component_voice_mode():
    thread = create_thread(data=dict(voice=True))
    delay = 5
    component = DelayComponent(delay=delay)
    component_start_entry = create_component_start_entry(
        component, thread=thread
    )
    say_event = SayEvent(text=f'<break time="{int(delay * 1000)}ms"/>')
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[say_event, flow_next_entry],
        thread=thread,
    )
