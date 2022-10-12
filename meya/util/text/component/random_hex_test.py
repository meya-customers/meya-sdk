import pytest

from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import verify_process_element
from meya.util.text.component.random_hex import RandomHexComponent


@pytest.mark.asyncio
async def test_random_hex_component():
    component = RandomHexComponent()
    component_start_entry = create_component_start_entry(component)
    flow_next_entry = create_flow_next_entry(
        component_start_entry, data=dict(result="~0")
    )
    await verify_process_element(
        component, component_start_entry, [flow_next_entry]
    )
