import pytest

from meya.button.spec import ButtonElementSpec
from meya.button.spec import ButtonEventSpec
from meya.button.trigger import ButtonTrigger
from meya.element.element_test import activate_triggers
from meya.element.element_test import create_bot
from meya.element.element_test import create_component_start_entry
from meya.element.element_test import create_flow_next_entry
from meya.element.element_test import create_thread
from meya.element.element_test import create_trigger_action_entry
from meya.element.element_test import to_spec
from meya.element.element_test import verify_process_element
from meya.event.composer_spec import ComposerEventSpec
from meya.event.composer_spec import ComposerFocus
from meya.event.composer_spec import ComposerVisibility
from meya.flow.component import FlowComponent
from meya.flow.element import FlowRef
from meya.icon.spec import IconElementSpec
from meya.icon.spec import IconEventSpec
from meya.tile.component.ask import ComposerElementSpec
from meya.tile.component.ask import TileAskComponent
from meya.tile.component.ask import TileElementSpec
from meya.tile.event.ask import TileAskEvent
from meya.tile.spec import TileButtonStyle
from meya.tile.spec import TileCell
from meya.tile.spec import TileEventSpec
from meya.tile.spec import TileImage
from meya.tile.spec import TileLayout


@pytest.mark.asyncio
async def test_tile_buttons():
    bot = create_bot()
    thread = create_thread()
    component = TileAskComponent(
        ask="Choose a tile button",
        tiles=[
            TileElementSpec(
                description="D1",
                buttons=[
                    ButtonElementSpec(text="B1", result={"k": 0}),
                    ButtonElementSpec(text="B2", result={"k": "1"}),
                ],
            ),
            TileElementSpec(
                title="T3", action=to_spec(FlowComponent(flow=FlowRef("f4")))
            ),
        ],
        button_style=TileButtonStyle.TEXT,
        quick_replies=["Cancel", "Help"],
        composer=ComposerElementSpec(
            placeholder="PLACE", visibility=ComposerVisibility.SHOW
        ),
        layout=TileLayout.ROW,
    )
    component_start_entry = create_component_start_entry(
        component, bot=bot, thread=thread
    )
    ask_tiles_event = TileAskEvent(
        button_style=TileButtonStyle.TEXT,
        composer=ComposerEventSpec(
            focus=ComposerFocus.BLUR,
            placeholder="PLACE",
            visibility=ComposerVisibility.SHOW,
        ),
        layout=TileLayout.ROW,
        quick_replies=[
            ButtonEventSpec(text="Cancel"),
            ButtonEventSpec(text="Help"),
        ],
        text="Choose a tile button",
        tiles=[
            TileEventSpec(
                buttons=[
                    ButtonEventSpec(button_id="b-~0", text="B1"),
                    ButtonEventSpec(button_id="b-~1", text="B2"),
                ],
                description="D1",
            ),
            TileEventSpec(button_id="b-~2", title="T3"),
        ],
    )
    triggers = activate_triggers(
        component_start_entry,
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_flow_next_entry(
                    component_start_entry, data=dict(result={"k": 0})
                )
            ),
            button_id="b-~0",
            text="B1",
        ),
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_flow_next_entry(
                    component_start_entry, data=dict(result={"k": "1"})
                )
            ),
            button_id="b-~1",
            text="B2",
        ),
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_component_start_entry(
                    FlowComponent(flow=FlowRef("f4")),
                    bot=bot,
                    thread=thread,
                    flow=component_start_entry.flow,
                    stack=component_start_entry.stack,
                )
            ),
            button_id="b-~2",
            text="T3",
        ),
    )
    await verify_process_element(
        component,
        component_start_entry,
        [ask_tiles_event, *triggers],
        thread=thread,
        extra_elements=[bot],
    )


@pytest.mark.asyncio
async def test_tile_magic_buttons():
    component = TileAskComponent(
        tiles=[
            TileElementSpec(
                buttons=[
                    ButtonElementSpec(text="B1", result=1),
                    ButtonElementSpec(button_id="b-2", result=2),
                ]
            ),
            TileElementSpec(button_id="b-3", result=3),
        ],
        quick_replies=[
            ButtonElementSpec(text="B4", result=4),
            ButtonElementSpec(button_id="b-5", result=5),
        ],
    )
    component_start_entry = create_component_start_entry(component)
    ask_tiles_event = TileAskEvent(
        button_style=None,
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        layout=None,
        text=None,
        tiles=[
            TileEventSpec(
                buttons=[ButtonEventSpec(text="B1", button_id="b-~0")]
            )
        ],
        quick_replies=[ButtonEventSpec(text="B4", button_id="b-~1")],
    )
    triggers = activate_triggers(
        component_start_entry,
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_flow_next_entry(
                    component_start_entry, data=dict(result=1)
                )
            ),
            button_id="b-~0",
            text="B1",
        ),
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_flow_next_entry(
                    component_start_entry, data=dict(result=2)
                )
            ),
            button_id="b-2",
        ),
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_flow_next_entry(
                    component_start_entry, data=dict(result=3)
                )
            ),
            button_id="b-3",
        ),
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_flow_next_entry(
                    component_start_entry, data=dict(result=4)
                )
            ),
            button_id="b-~1",
            text="B4",
        ),
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_flow_next_entry(
                    component_start_entry, data=dict(result=5)
                )
            ),
            button_id="b-5",
        ),
    )
    await verify_process_element(
        component, component_start_entry, [ask_tiles_event, *triggers]
    )


@pytest.mark.asyncio
async def test_tile_text_buttons():
    component = TileAskComponent(
        tiles=[
            TileElementSpec(title="T1"),
            TileElementSpec(description="D2"),
            TileElementSpec(buttons=["B1", ButtonElementSpec(text="B2")]),
        ]
    )
    component_start_entry = create_component_start_entry(component)
    ask_tiles_event = TileAskEvent(
        button_style=None,
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        layout=None,
        text=None,
        tiles=[
            TileEventSpec(title="T1"),
            TileEventSpec(description="D2"),
            TileEventSpec(
                buttons=[
                    ButtonEventSpec(text="B1"),
                    ButtonEventSpec(text="B2"),
                ]
            ),
        ],
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        component, component_start_entry, [ask_tiles_event, flow_next_entry]
    )


@pytest.mark.asyncio
async def test_tile_static_buttons():
    component = TileAskComponent(
        tiles=[
            TileElementSpec(
                title="T1", button_id="b-1", context=dict(product="p-1")
            ),
            TileElementSpec(
                buttons=[ButtonElementSpec(text="B2", button_id="b-2")]
            ),
        ],
        quick_replies=[
            ButtonElementSpec(
                text="B3", button_id="b-3", context=dict(product="p-3")
            )
        ],
    )
    component_start_entry = create_component_start_entry(component)
    ask_tiles_event = TileAskEvent(
        button_style=None,
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        layout=None,
        quick_replies=[
            ButtonEventSpec(
                text="B3", button_id="b-3", context=dict(product="p-3")
            )
        ],
        text=None,
        tiles=[
            TileEventSpec(
                title="T1", button_id="b-1", context=dict(product="p-1")
            ),
            TileEventSpec(
                buttons=[ButtonEventSpec(text="B2", button_id="b-2")]
            ),
        ],
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        component, component_start_entry, [ask_tiles_event, flow_next_entry]
    )


@pytest.mark.asyncio
async def test_tile_links():
    component = TileAskComponent(
        tiles=[
            TileElementSpec(
                title="T1",
                buttons=[ButtonElementSpec(text="B3", url="http://u1.org")],
            ),
            TileElementSpec(
                url="http://u2.org", image=TileImage(url="http://i1.org")
            ),
        ]
    )
    component_start_entry = create_component_start_entry(component)
    ask_tiles_event = TileAskEvent(
        button_style=None,
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        layout=None,
        text=None,
        tiles=[
            TileEventSpec(
                buttons=[ButtonEventSpec(text="B3", url="http://u1.org")],
                title="T1",
            ),
            TileEventSpec(
                image=TileImage(url="http://i1.org"), url="http://u2.org"
            ),
        ],
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        component, component_start_entry, [ask_tiles_event, flow_next_entry]
    )


@pytest.mark.asyncio
async def test_tile_javascript():
    component = TileAskComponent(
        tiles=[
            TileElementSpec(
                title="T1",
                buttons=[
                    ButtonElementSpec(
                        text="B3", result={"k": True}, javascript="alert('hi')"
                    )
                ],
            ),
            TileElementSpec(javascript="console.log('l')", title="JS"),
        ]
    )
    component_start_entry = create_component_start_entry(component)
    ask_tiles_event = TileAskEvent(
        button_style=None,
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        layout=None,
        text=None,
        tiles=[
            TileEventSpec(
                buttons=[
                    ButtonEventSpec(
                        button_id="b-~0", text="B3", javascript="alert('hi')"
                    )
                ],
                title="T1",
            ),
            TileEventSpec(
                button_id="b-~1", javascript="console.log('l')", title="JS"
            ),
        ],
    )
    triggers = activate_triggers(
        component_start_entry,
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_flow_next_entry(
                    component_start_entry, data=dict(result={"k": True})
                )
            ),
            button_id="b-~0",
            text="B3",
        ),
    )
    await verify_process_element(
        component, component_start_entry, [ask_tiles_event, *triggers]
    )


@pytest.mark.asyncio
async def test_tile_cells():
    component = TileAskComponent(
        tiles=[
            TileElementSpec(
                result={"k": "2"},
                rows=[
                    [
                        TileCell(cell="C1", value="V1"),
                        TileCell(cell="C2", value="V2"),
                    ],
                    [TileCell(cell="C3", value="V3")],
                ],
            )
        ]
    )
    component_start_entry = create_component_start_entry(component)
    ask_tiles_event = TileAskEvent(
        button_style=None,
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        layout=None,
        text=None,
        tiles=[
            TileEventSpec(
                button_id="b-~0",
                rows=[
                    [
                        TileCell(cell="C1", value="V1"),
                        TileCell(cell="C2", value="V2"),
                    ],
                    [TileCell(cell="C3", value="V3")],
                ],
            )
        ],
    )
    triggers = activate_triggers(
        component_start_entry,
        ButtonTrigger(
            action=create_trigger_action_entry(
                create_flow_next_entry(
                    component_start_entry, data=dict(result={"k": "2"})
                )
            ),
            button_id="b-~0",
        ),
    )
    await verify_process_element(
        component, component_start_entry, [ask_tiles_event, *triggers]
    )


@pytest.mark.asyncio
async def test_tile_icons():
    component = TileAskComponent(
        tiles=[
            TileElementSpec(
                title="T1",
                icon="streamline-regular/52-arrows-diagrams/01-arrows/arrow-left-1.svg",
            ),
            TileElementSpec(
                icon=IconElementSpec(
                    url="https://fonts.gstatic.com/s/i/materialicons/3d_rotation/v9/24px.svg?download",
                    color="red",
                )
            ),
            TileElementSpec(
                buttons=[
                    ButtonElementSpec(
                        text="B1",
                        icon="streamline-regular/52-arrows-diagrams/01-arrows/arrow-left-1.svg",
                    ),
                    ButtonElementSpec(
                        icon=IconElementSpec(
                            url="https://fonts.gstatic.com/s/i/materialicons/3d_rotation/v9/24px.svg?download",
                            color="red",
                        )
                    ),
                ]
            ),
        ]
    )
    component_start_entry = create_component_start_entry(component)
    ask_tiles_event = TileAskEvent(
        button_style=None,
        composer=ComposerEventSpec(focus=ComposerFocus.BLUR),
        layout=None,
        text=None,
        tiles=[
            TileEventSpec(
                title="T1",
                icon=IconEventSpec(
                    url=f"https://cdn-test.meya.ai/icon/streamline-regular/52-arrows-diagrams/01-arrows/arrow-left-1.svg"
                ),
            ),
            TileEventSpec(
                icon=IconEventSpec(
                    url="https://fonts.gstatic.com/s/i/materialicons/3d_rotation/v9/24px.svg?download",
                    color="red",
                )
            ),
            TileEventSpec(
                buttons=[
                    ButtonEventSpec(
                        text="B1",
                        icon=IconEventSpec(
                            url=f"https://cdn-test.meya.ai/icon/streamline-regular/52-arrows-diagrams/01-arrows/arrow-left-1.svg"
                        ),
                    ),
                    ButtonEventSpec(
                        icon=IconEventSpec(
                            url="https://fonts.gstatic.com/s/i/materialicons/3d_rotation/v9/24px.svg?download",
                            color="red",
                        )
                    ),
                ]
            ),
        ],
    )
    flow_next_entry = create_flow_next_entry(component_start_entry)
    await verify_process_element(
        component, component_start_entry, [ask_tiles_event, flow_next_entry]
    )
