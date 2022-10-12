import pytest

from meya.csp.component.session.end import SessionEndComponent
from meya.csp.event.session.end import SessionEndEvent
from meya.csp.integration import CspIntegration
from meya.csp.integration import CspIntegrationRef
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import verify_process_element


@pytest.mark.asyncio
async def test_end_agent_session_component():
    integration = CspIntegration(id="test-csp")
    component = SessionEndComponent(
        integration=CspIntegrationRef(integration.id)
    )
    component_start_entry = create_component_start_entry(component)
    end_session_event = SessionEndEvent(csp_integration_id=integration.id)
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[end_session_event, flow_next_entry],
        extra_elements=[integration],
    )
