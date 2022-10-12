import pytest

from meya.component.element import ComponentErrorResponse
from meya.component.element import ComponentOkResponse
from meya.element.element_test import activate_triggers
from meya.element.element_test import create_component_next_entry
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import create_user
from meya.element.element_test import test_type_registry
from meya.element.element_test import verify_process_element
from meya.event.composer_spec import ComposerEventSpec
from meya.event.composer_spec import ComposerFocus
from meya.form.component.select import SelectComponent
from meya.form.event.ask import Field
from meya.form.event.ask import FieldType
from meya.form.event.ask import FormAskEvent
from meya.form.event.error import FormErrorEvent
from meya.form.event.ok import FormOkEvent
from meya.form.event.submit import FormSubmitEvent
from meya.form.spec import SelectOptionElementSpec
from meya.form.spec import SelectOptionEventSpec
from meya.form.trigger import FormTrigger
from meya.icon.spec import IconEventSpec
from meya.util.dict import to_dict
from typing import Any
from typing import List


@pytest.mark.asyncio
async def test_component_single_start():
    component = SelectComponent(
        select="Select?",
        icon="streamline-regular/17-users/04-geometric-full body-single user-woman/single-woman-question.svg",
        name="order",
        options=[
            "First",
            "Second",
            "Third",
            SelectOptionElementSpec(text="Fourth"),
        ],
    )
    component_start_entry = create_component_start_entry(component)
    form_event = FormAskEvent(
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        form_id="form-~0",
        fields=[
            Field(
                name="order",
                autocomplete="off",
                icon=IconEventSpec(
                    url=f"https://cdn-test.meya.ai/icon/streamline-regular/17-users/04-geometric-full-body-single-user-woman/single-woman-question.svg"
                ),
                placeholder=None,
                label="Select?",
                no_results_text="No results",
                required=True,
                type=FieldType.SELECT,
                custom=False,
                search=False,
                multi=False,
                default=None,
                options=[
                    SelectOptionEventSpec(text="First"),
                    SelectOptionEventSpec(text="Second"),
                    SelectOptionEventSpec(text="Third"),
                    SelectOptionEventSpec(text="Fourth"),
                ],
            )
        ],
    )
    triggers = activate_triggers(
        component_start_entry,
        FormTrigger(
            action=create_trigger_action_entry(
                create_component_next_entry(component_start_entry)
            ),
            form_id="form-~0",
        ),
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[form_event, *triggers],
    )


@pytest.mark.asyncio
async def test_component_multi_start():
    component = SelectComponent(
        multi=True,
        default=["A", "B"],
        options=["A", SelectOptionElementSpec(text="B", value=2), "C"],
    )
    component_start_entry = create_component_start_entry(component)
    form_event = FormAskEvent(
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        form_id="form-~0",
        fields=[
            Field(
                name="select",
                autocomplete="off",
                icon=None,
                placeholder=None,
                label="Select",
                no_results_text="No results",
                required=True,
                type=FieldType.SELECT,
                custom=False,
                search=False,
                multi=True,
                default=["A", "B"],
                options=[
                    SelectOptionEventSpec(text="A"),
                    SelectOptionEventSpec(text="B"),
                    SelectOptionEventSpec(text="C"),
                ],
            )
        ],
    )
    triggers = activate_triggers(
        component_start_entry,
        FormTrigger(
            action=create_trigger_action_entry(
                create_component_next_entry(component_start_entry)
            ),
            form_id="form-~0",
        ),
    )
    await verify_process_element(
        element=component,
        sub_entry=component_start_entry,
        expected_pub_entries=[form_event, *triggers],
    )


@pytest.mark.parametrize(
    ("custom", "value", "result"),
    [
        (False, "A", "A"),
        (False, "B", "B"),
        (False, "C", None),
        (True, "D", [1, 2, 3]),
        (True, "E", "E"),
    ],
)
@pytest.mark.asyncio
async def test_component_single_next(custom: bool, value: str, result: Any):
    component = SelectComponent(
        custom=custom,
        options=[
            "A",
            SelectOptionElementSpec(text="B"),
            SelectOptionElementSpec(text="C", value=None),
            SelectOptionElementSpec(text="D", value=[1, 2, 3]),
        ],
    )
    form_submit_event = FormSubmitEvent(
        form_id="form_1",
        fields={"select": value},
        user_id=create_user().id,
        thread_id="t-0",
    )
    component_next_entry = create_component_next_entry(
        create_component_start_entry(component),
        data={
            FormTrigger.EVENT_KEY: form_submit_event.to_typed_dict(
                test_type_registry
            ),
            FormTrigger.RESULT_KEY: form_submit_event.fields,
        },
    )
    flow_next_entry = create_flow_next_entry(
        component_next_entry, data=to_dict(ComponentOkResponse(result=result))
    )
    form_ok_event = FormOkEvent(form_id="form_1")
    await verify_process_element(
        element=component,
        sub_entry=component_next_entry,
        expected_pub_entries=[form_ok_event, flow_next_entry],
    )


@pytest.mark.parametrize(
    ("custom", "value", "result"),
    [
        (False, ["A"], ["A"]),
        (False, ["B", "C"], ["B", None]),
        (True, ["D", "A"], [[1, 2, 3], "A"]),
        # (True, ["E", "C"], ["E", None]), TODO Add multi+custom support
    ],
)
@pytest.mark.asyncio
async def test_component_multi_next(
    custom: bool, value: List[str], result: List[Any]
):
    # TODO Add multi+custom support
    custom = False
    component = SelectComponent(
        custom=custom,
        multi=True,
        options=[
            "A",
            SelectOptionElementSpec(text="B"),
            SelectOptionElementSpec(text="C", value=None),
            SelectOptionElementSpec(text="D", value=[1, 2, 3]),
        ],
    )
    form_submit_event = FormSubmitEvent(
        form_id="form_1",
        fields={"select": value},
        user_id=create_user().id,
        thread_id="t-0",
    )
    component_next_entry = create_component_next_entry(
        create_component_start_entry(component),
        data={
            FormTrigger.EVENT_KEY: form_submit_event.to_typed_dict(
                test_type_registry
            ),
            FormTrigger.RESULT_KEY: form_submit_event.fields,
        },
    )
    flow_next_entry = create_flow_next_entry(
        component_next_entry, data=to_dict(ComponentOkResponse(result=result))
    )
    form_ok_event = FormOkEvent(form_id="form_1")
    await verify_process_element(
        element=component,
        sub_entry=component_next_entry,
        expected_pub_entries=[form_ok_event, flow_next_entry],
    )


@pytest.mark.parametrize(
    ("custom", "value"),
    [(True, None), (True, ["A"]), (True, "B"), (False, "C")],
)
@pytest.mark.asyncio
async def test_component_single_invalid_value(custom: bool, value: Any):
    component = SelectComponent(
        custom=custom,
        select="Select?",
        options=["A", SelectOptionElementSpec(text="B", disabled=True)],
    )
    form_submit_event = FormSubmitEvent(
        form_id="form_1",
        fields={"select": value},
        user_id=create_user().id,
        thread_id="t-0",
    )
    component_next_entry = create_component_next_entry(
        create_component_start_entry(component),
        data={
            FormTrigger.EVENT_KEY: form_submit_event.to_typed_dict(
                test_type_registry
            ),
            FormTrigger.RESULT_KEY: form_submit_event.fields,
        },
    )
    form_error_event = FormErrorEvent(
        form_id="form_1", fields={"select": "Invalid value selected"}
    )
    triggers = activate_triggers(
        component_next_entry,
        FormTrigger(
            action=create_trigger_action_entry(
                create_component_next_entry(
                    component_next_entry,
                    data=to_dict(
                        ComponentErrorResponse(result=value, retry_count=1)
                    ),
                )
            ),
            form_id="form_1",
        ),
    )
    await verify_process_element(
        element=component,
        sub_entry=component_next_entry,
        expected_pub_entries=[form_error_event, *triggers],
    )


@pytest.mark.parametrize(
    ("custom", "value"),
    [
        (True, None),
        (True, "A"),
        (True, []),
        (True, ["B"]),
        (False, ["A", "F"]),
    ],
)
@pytest.mark.asyncio
async def test_component_multi_invalid_value(custom: bool, value: Any):
    # TODO Add multi+custom support
    custom = False
    component = SelectComponent(
        custom=custom,
        multi=True,
        options=["A", SelectOptionElementSpec(text="B", disabled=True), "C"],
    )
    form_submit_event = FormSubmitEvent(
        form_id="form_1",
        fields={"select": value},
        user_id=create_user().id,
        thread_id="t-0",
    )
    component_next_entry = create_component_next_entry(
        create_component_start_entry(component),
        data={
            FormTrigger.EVENT_KEY: form_submit_event.to_typed_dict(
                test_type_registry
            ),
            FormTrigger.RESULT_KEY: form_submit_event.fields,
        },
    )
    form_error_event = FormErrorEvent(
        form_id="form_1", fields={"select": "Invalid value selected"}
    )
    triggers = activate_triggers(
        component_next_entry,
        FormTrigger(
            action=create_trigger_action_entry(
                create_component_next_entry(
                    component_next_entry,
                    data=to_dict(
                        ComponentErrorResponse(result=value, retry_count=1)
                    ),
                )
            ),
            form_id="form_1",
        ),
    )
    await verify_process_element(
        element=component,
        sub_entry=component_next_entry,
        expected_pub_entries=[form_error_event, *triggers],
    )
