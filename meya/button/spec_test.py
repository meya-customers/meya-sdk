import pytest

from meya.button.spec import ButtonElementSpec
from meya.button.spec import ButtonType
from unittest.mock import MagicMock


@pytest.mark.parametrize(
    ("button", "expected_magic", "expected_type"),
    [
        (ButtonElementSpec(text="x"), False, ButtonType.TEXT),
        (
            ButtonElementSpec(text="x", url="https://www.domain.com"),
            False,
            ButtonType.URL,
        ),
        (
            ButtonElementSpec(url="https://www.domain.com"),
            False,
            ButtonType.URL,
        ),
        (
            ButtonElementSpec(text="x", javascript="alert('wow');"),
            False,
            ButtonType.STATIC,
        ),
        (
            ButtonElementSpec(text="x", action=MagicMock()),
            False,
            ButtonType.ACTION,
        ),
        (
            ButtonElementSpec(
                text="x", action=MagicMock(), result={MagicMock(): MagicMock()}
            ),
            False,
            ButtonType.ACTION,
        ),
        (
            ButtonElementSpec(text="x", type=ButtonType.ACTION),
            False,
            ButtonType.ACTION,
        ),
        (
            ButtonElementSpec(icon=MagicMock(), type=ButtonType.ACTION),
            False,
            ButtonType.ACTION,
        ),
        (
            ButtonElementSpec(text="x", magic=True, type=ButtonType.ACTION),
            True,
            ButtonType.ACTION,
        ),
        (ButtonElementSpec(type=ButtonType.ACTION), True, ButtonType.ACTION),
        (
            ButtonElementSpec(text="x", button_id=MagicMock()),
            False,
            ButtonType.STATIC,
        ),
        (ButtonElementSpec(button_id=MagicMock()), True, ButtonType.STATIC),
        (
            ButtonElementSpec(
                text="x", action=MagicMock(), javascript="alert('wow');"
            ),
            False,
            ButtonType.ACTION,
        ),
        (
            ButtonElementSpec(
                text="x",
                result={MagicMock(): MagicMock()},
                javascript="alert('wow');",
            ),
            False,
            ButtonType.FLOW_NEXT,
        ),
        (
            ButtonElementSpec(text="x", type=ButtonType.FLOW_NEXT),
            False,
            ButtonType.FLOW_NEXT,
        ),
        (
            ButtonElementSpec(
                text="x", javascript="alert('wow');", type=ButtonType.FLOW_NEXT
            ),
            False,
            ButtonType.FLOW_NEXT,
        ),
        (
            ButtonElementSpec(text="x", type=ButtonType.COMPONENT_NEXT),
            False,
            ButtonType.COMPONENT_NEXT,
        ),
        (
            ButtonElementSpec(
                text="x",
                javascript="alert('wow');",
                type=ButtonType.COMPONENT_NEXT,
            ),
            False,
            ButtonType.COMPONENT_NEXT,
        ),
    ],
)
def test_button_spec_type(
    button: ButtonElementSpec, expected_magic: bool, expected_type: ButtonType
):
    assert button.computed_magic == expected_magic
    assert button.computed_type == expected_type
