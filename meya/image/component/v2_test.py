import pytest

from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import verify_process_element
from meya.image.component.v2 import ImageV2Component
from meya.image.event import ImageEvent


@pytest.mark.asyncio
async def test_image_component():
    url = "image.jpg"
    component = ImageV2Component(image=url, alt="image")
    component_start_entry = create_component_start_entry(component)
    image_event = ImageEvent(url=url, alt="image")
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[image_event, flow_next_entry],
    )
