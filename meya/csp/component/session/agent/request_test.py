import pytest

from meya.csp.component.session.agent.request import AgentRequestComponent
from meya.csp.event.session.agent.request import AgentRequestEvent
from meya.csp.integration import CspIntegration
from meya.csp.integration import CspIntegrationRef
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import verify_process_element
from meya.text.event.say import SayEvent


@pytest.mark.asyncio
async def test_request_agent_component():
    integration = CspIntegration(id="test-csp")
    component = AgentRequestComponent(
        integration=CspIntegrationRef(integration.id),
        say="Transferring you to an agent",
        note="Test not for the agent",
        timeout=123,
        timeout_flow=None,
        data=dict(custom="value"),
    )
    component_start_entry = create_component_start_entry(component)
    say_event = SayEvent(text="Transferring you to an agent")
    agent_request_event = AgentRequestEvent(
        data=dict(custom="value"),
        csp_integration_id=integration.id,
        note="Test not for the agent",
        timeout=123,
        timeout_flow=None,
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[say_event, agent_request_event, flow_next_entry],
        extra_elements=[integration],
    )
