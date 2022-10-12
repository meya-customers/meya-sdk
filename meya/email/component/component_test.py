import pytest

from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import verify_process_element
from meya.email.component import EmailComponent
from meya.email.event import EmailEvent


@pytest.mark.asyncio
async def test_email_component():
    subject = "test subject"
    html = "<h1>Test Html</h1>"
    text = "text test html"
    message_id = "id-1"
    component = EmailComponent(
        subject=subject, html=html, text=text, message_id=message_id
    )
    component_start_entry = create_component_start_entry(component)
    say_event = EmailEvent(
        subject=subject, html=html, text=text, message_id=message_id
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[say_event, flow_next_entry],
    )
