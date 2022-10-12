import pytest

from meya.csp.component.monitor import MonitorComponent
from meya.csp.event.monitor import MonitorEvent
from meya.csp.integration import CspIntegration
from meya.csp.integration import CspIntegrationRef
from meya.element.element_test import create_bot
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_thread
from meya.element.element_test import verify_process_element


@pytest.mark.asyncio
async def test_csp_monitor_component():
    bot = create_bot()
    thread = create_thread()
    integration = CspIntegration(id="test-csp")
    component = MonitorComponent(
        integration=CspIntegrationRef(integration.id),
        note="Test not for the agent",
        data={},
    )
    component_start_entry = create_component_start_entry(
        component, bot=bot, thread=thread
    )
    csp_track_event = MonitorEvent(
        data={},
        csp_integration_id=integration.id,
        note="Test not for the agent",
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[csp_track_event, flow_next_entry],
        thread=thread,
        extra_elements=[bot, integration],
    )
