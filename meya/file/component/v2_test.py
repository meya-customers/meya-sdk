import pytest

from meya.button.spec import ButtonEventSpec
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import verify_process_element
from meya.event.composer_spec import ComposerElementSpec
from meya.event.composer_spec import ComposerEventSpec
from meya.file.component.v2 import FileV2Component
from meya.file.event import FileEvent
from meya.icon.spec import IconEventSpec


@pytest.mark.asyncio
async def test_file_component():
    component = FileV2Component(
        file="http://example.org/file.pdf",
        name="file.pdf",
        icon="streamline-regular/14-music-audio/18-audio-files/audio-file-mid.svg",
        quick_replies=["Restart"],
        composer=ComposerElementSpec(placeholder="Anything else?"),
    )
    component_start_entry = create_component_start_entry(component)
    file_event = FileEvent(
        composer=ComposerEventSpec(placeholder="Anything else?"),
        filename="file.pdf",
        icon=IconEventSpec(
            url=f"https://cdn-test.meya.ai/icon/streamline-regular/14-music-audio/18-audio-files/audio-file-mid.svg"
        ),
        quick_replies=[ButtonEventSpec(text="Restart")],
        url="http://example.org/file.pdf",
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        component, component_start_entry, [file_event, flow_next_entry]
    )
