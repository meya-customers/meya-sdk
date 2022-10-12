import pytest

from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_user
from meya.element.element_test import verify_process_element
from meya.file.component.load import FileLoadComponent
from pathlib import Path
from tempfile import TemporaryDirectory


@pytest.mark.asyncio
async def test_load_no_context():
    with TemporaryDirectory() as temp_dir:
        temp_file_path = Path(temp_dir) / "file"
        with temp_file_path.open("w") as temp_file:
            temp_file.write("abc (@ x )")
        component = FileLoadComponent(file_path=str(temp_file_path))
        component_start_entry = create_component_start_entry(component)
        flow_next_entry = create_flow_next_entry(
            component_start_entry, data=dict(result="abc (@ x )")
        )
        await verify_process_element(
            component, component_start_entry, [flow_next_entry]
        )


@pytest.mark.asyncio
async def test_load_custom_context():
    with TemporaryDirectory() as temp_dir:
        temp_file_path = Path(temp_dir) / "file"
        with temp_file_path.open("w") as temp_file:
            temp_file.write("abc (@ x | e ) (@ y + 3 )")
        component = FileLoadComponent(
            file_path=str(temp_file_path),
            template=True,
            template_context=dict(x="xyz<", y=8),
        )
        component_start_entry = create_component_start_entry(component)
        flow_next_entry = create_flow_next_entry(
            component_start_entry, data=dict(result="abc xyz&lt; 11")
        )
        await verify_process_element(
            component, component_start_entry, [flow_next_entry]
        )


@pytest.mark.asyncio
async def test_load_builtin_context():
    with TemporaryDirectory() as temp_dir:
        temp_file_path = Path(temp_dir) / "file"
        with temp_file_path.open("w") as temp_file:
            temp_file.write("(@ flow.x | tojson ) (@ user.y | upper )")
        component = FileLoadComponent(
            file_path=str(temp_file_path), template=True
        )
        user = create_user(data=dict(y="Hello"))
        component_start_entry = create_component_start_entry(
            component, data=dict(x=[1, "\n"])
        )
        flow_next_entry = create_flow_next_entry(
            component_start_entry, data=dict(result='[1, "\\n"] HELLO')
        )
        await verify_process_element(
            component, component_start_entry, [flow_next_entry], user=user
        )
