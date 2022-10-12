import pytest

from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import verify_process_element
from meya.util.text.component.split_name import SplitNameComponent


@pytest.mark.parametrize(
    ("name", "first_name", "last_name"),
    [
        ("Bill Gates", "Bill", "Gates"),
        ("Madonna", "Madonna", ""),
        ("Cuba Gooding Jr.", "Cuba", "Gooding Jr."),
        ("", "", ""),
    ],
)
@pytest.mark.asyncio
async def test_split_name_component(
    name: str, first_name: str, last_name: str
):
    component = SplitNameComponent(name=name)
    component_start_entry = create_component_start_entry(component)
    flow_next_entry = create_flow_next_entry(
        component_start_entry,
        data=dict(result=dict(first_name=first_name, last_name=last_name)),
    )
    await verify_process_element(
        component, component_start_entry, [flow_next_entry]
    )
