import pytest

from meya.date.component.input.input import DateInputComponent
from meya.widget.component.component import WidgetInputValidationError


def _make_component(**kwargs) -> DateInputComponent:
    """Create a DateInputComponent with defaults for testing validate_input_data."""
    defaults = dict(
        required=False,
        min=None,
        max=None,
        error_message="Please select a valid date.",
    )
    defaults.update(kwargs)
    component = object.__new__(DateInputComponent)
    for key, value in defaults.items():
        object.__setattr__(component, key, value)
    return component


@pytest.mark.asyncio
async def test_valid_date():
    component = _make_component(input_data="2025-06-15")
    result = await component.validate_input_data()
    assert result == "2025-06-15"


@pytest.mark.asyncio
async def test_empty_not_required():
    component = _make_component(input_data="", required=False)
    result = await component.validate_input_data()
    assert result == ""


@pytest.mark.asyncio
async def test_empty_required():
    component = _make_component(input_data="", required=True)
    with pytest.raises(WidgetInputValidationError):
        await component.validate_input_data()


@pytest.mark.asyncio
async def test_invalid_string():
    component = _make_component(input_data="not-a-date")
    with pytest.raises(WidgetInputValidationError):
        await component.validate_input_data()


@pytest.mark.asyncio
async def test_date_before_min():
    component = _make_component(input_data="2020-01-01", min="2021-01-01")
    with pytest.raises(WidgetInputValidationError):
        await component.validate_input_data()


@pytest.mark.asyncio
async def test_date_after_max():
    component = _make_component(input_data="2030-12-31", max="2029-12-31")
    with pytest.raises(WidgetInputValidationError):
        await component.validate_input_data()


@pytest.mark.asyncio
async def test_date_within_range():
    component = _make_component(
        input_data="2025-06-15", min="2025-01-01", max="2025-12-31"
    )
    result = await component.validate_input_data()
    assert result == "2025-06-15"


@pytest.mark.asyncio
async def test_date_at_min_boundary():
    component = _make_component(input_data="2025-01-01", min="2025-01-01")
    result = await component.validate_input_data()
    assert result == "2025-01-01"


@pytest.mark.asyncio
async def test_date_at_max_boundary():
    component = _make_component(input_data="2025-12-31", max="2025-12-31")
    result = await component.validate_input_data()
    assert result == "2025-12-31"


@pytest.mark.asyncio
async def test_malformed_min_raises():
    component = _make_component(input_data="2025-06-15", min="not-a-date")
    with pytest.raises(ValueError, match="invalid `min`"):
        await component.validate_input_data()


@pytest.mark.asyncio
async def test_malformed_max_raises():
    component = _make_component(input_data="2025-06-15", max="2025/12/31")
    with pytest.raises(ValueError, match="invalid `max`"):
        await component.validate_input_data()
