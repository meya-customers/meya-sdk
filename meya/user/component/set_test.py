import pytest

from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_log_message_entry
from meya.element.element_test import create_user
from meya.element.element_test import create_user_changes
from meya.element.element_test import verify_process_element
from meya.log.level import Level
from meya.user.component.set import UserSetComponent
from typing import Union


@pytest.mark.parametrize(
    ("flow_data", "user_set", "existing_user_data", "user_updates"),
    [
        ({"result": "test@meya.ai"}, "email", {}, {"email": "test@meya.ai"}),
        ({"result": "test@meya.ai"}, "email", {"email": "test@meya.ai"}, {}),
        (
            {},
            {"email": "test@meya.ai", "foo": "bar"},
            {},
            {"email": "test@meya.ai", "foo": "bar"},
        ),
        (
            {},
            {"email": "test@meya.ai", "foo": "bar"},
            {"foo": "bar"},
            {"email": "test@meya.ai"},
        ),
    ],
)
@pytest.mark.asyncio
async def test_user_set_component(
    flow_data: dict,
    user_set: Union[str, dict],
    existing_user_data: dict,
    user_updates: dict,
):
    component = UserSetComponent(user_set=user_set)
    component_start_entry = create_component_start_entry(
        component, data=flow_data
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    user = create_user(data=existing_user_data)
    user_changes = create_user_changes(user, user_updates)
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[flow_next_entry, *user_changes],
        user=user,
    )


@pytest.mark.asyncio
async def test_user_set_component_no_result():
    """
    When `user_set` is a string then the component expects the `result` key
    to be present in `flow_data` otherwise it logs and error.
    """
    user_set = "email"
    component = UserSetComponent(user_set=user_set)
    component_start_entry = create_component_start_entry(
        component, data={"K1": "V1"}
    )
    log_entry = create_log_message_entry(
        Level.ERROR,
        (
            f'Could not set user scope property "{user_set}"'
            f" because flow.result is not set"
        ),
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[log_entry],
    )
