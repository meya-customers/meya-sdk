import pytest

from meya.button.spec import ButtonElementSpec
from meya.tile.spec import TileCell
from meya.tile.spec import TileElementSpec
from unittest.mock import MagicMock


@pytest.mark.parametrize(
    ("tile", "expected_magic"),
    [
        (TileElementSpec(button_id=MagicMock()), True),
        (
            TileElementSpec(
                buttons=[ButtonElementSpec(button_id=MagicMock())]
            ),
            True,
        ),
        (TileElementSpec(button_id=MagicMock(), rows=[[]]), True),
        (TileElementSpec(title=MagicMock(), button_id=MagicMock()), False),
        (
            TileElementSpec(
                buttons=[
                    ButtonElementSpec(text=MagicMock(), button_id=MagicMock())
                ]
            ),
            False,
        ),
        (TileElementSpec(buttons=["x"]), False),
        (
            TileElementSpec(
                button_id=MagicMock(),
                rows=[[TileCell(cell=MagicMock(), value=MagicMock())]],
            ),
            False,
        ),
        (TileElementSpec(title=MagicMock()), False),
        (TileElementSpec(description=MagicMock()), False),
        (TileElementSpec(icon=MagicMock()), False),
        (TileElementSpec(image=MagicMock()), False),
        (TileElementSpec(url=MagicMock()), False),
    ],
)
def test_tile_spec_magic(tile: TileElementSpec, expected_magic: bool):
    print(tile)
    assert tile.computed_magic == expected_magic
