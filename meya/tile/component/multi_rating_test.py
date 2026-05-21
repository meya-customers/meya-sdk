import pytest

from meya.tile.component.multi_rating import MultiRatingComponent
from meya.tile.component.multi_rating import RatingGroupElementSpec
from meya.tile.component.rating import RatingType
from meya.widget.component.component import WidgetInputValidationError


def _make_component(**kwargs) -> MultiRatingComponent:
    """Create a MultiRatingComponent with defaults for testing validate_input_data."""
    defaults = dict(
        required=False,
        groups=[
            RatingGroupElementSpec(title="Quality", rating=RatingType.STARS),
            RatingGroupElementSpec(title="Support", rating=RatingType.THUMBS),
        ],
        error_message="Please provide all ratings.",
    )
    defaults.update(kwargs)
    component = object.__new__(MultiRatingComponent)
    for key, value in defaults.items():
        object.__setattr__(component, key, value)
    return component


@pytest.mark.asyncio
async def test_valid_input():
    component = _make_component(input_data=[4, 1])
    result = await component.validate_input_data()
    assert result == [4, 1]


@pytest.mark.asyncio
async def test_valid_input_with_none_not_required():
    component = _make_component(input_data=[4, None], required=False)
    result = await component.validate_input_data()
    assert result == [4, None]


@pytest.mark.asyncio
async def test_missing_selection_required():
    component = _make_component(input_data=[4, None], required=True)
    with pytest.raises(WidgetInputValidationError):
        await component.validate_input_data()


@pytest.mark.asyncio
async def test_all_none_required():
    component = _make_component(input_data=[None, None], required=True)
    with pytest.raises(WidgetInputValidationError):
        await component.validate_input_data()


@pytest.mark.asyncio
async def test_all_none_not_required():
    component = _make_component(input_data=[None, None], required=False)
    result = await component.validate_input_data()
    assert result == [None, None]


@pytest.mark.asyncio
async def test_wrong_length():
    component = _make_component(input_data=[4])
    with pytest.raises(AssertionError):
        await component.validate_input_data()


@pytest.mark.asyncio
async def test_not_a_list():
    component = _make_component(input_data="invalid")
    with pytest.raises(AssertionError):
        await component.validate_input_data()


@pytest.mark.asyncio
async def test_three_groups():
    groups = [
        RatingGroupElementSpec(title="Speed", rating=RatingType.STARS),
        RatingGroupElementSpec(title="Quality", rating=RatingType.FACES),
        RatingGroupElementSpec(title="Support", rating=RatingType.THUMBS),
    ]
    component = _make_component(
        groups=groups, input_data=[5, 2, -1], required=True
    )
    result = await component.validate_input_data()
    assert result == [5, 2, -1]


@pytest.mark.asyncio
async def test_out_of_range_score_rejected():
    # Stars allow 1..5, faces allow -2..2 — submit values outside both sets.
    component = _make_component(input_data=[99, 1])
    with pytest.raises(WidgetInputValidationError):
        await component.validate_input_data()


@pytest.mark.asyncio
async def test_wrong_type_score_rejected():
    component = _make_component(input_data=["not-a-number", 1])
    with pytest.raises(WidgetInputValidationError):
        await component.validate_input_data()


@pytest.mark.asyncio
async def test_custom_option_with_none_score_rejected_at_validate():
    from meya.tile.component.rating import Option

    groups = [
        RatingGroupElementSpec(
            title="Custom",
            rating=RatingType.CUSTOM,
            options=[Option(text="ok"), Option(text="bad", score=0)],
        ),
    ]
    component = _make_component(groups=groups)
    with pytest.raises(Exception, match="score"):
        component.validate()


def test_empty_groups_rejected_at_validate():
    component = _make_component(groups=[])
    with pytest.raises(Exception, match="groups"):
        component.validate()
