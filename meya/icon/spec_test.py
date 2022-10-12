import pytest

from meya.env_test import patch_env
from meya.icon.spec import IconElementSpec
from meya.icon.spec import IconElementSpecUnion
from meya.icon.spec import IconEventSpec
from typing import Optional


@pytest.mark.parametrize(
    ("icon_element_spec", "icon_event_spec"),
    [
        (None, None),
        (
            "streamline-regular/01-interface essential/33-form-validation/check-circle-1.svg",
            IconEventSpec(
                url=f"https://cdn-test.meya.ai/icon/streamline-regular/01-interface-essential/33-form-validation/check-circle-1.svg"
            ),
        ),
        (
            "streamline-regular/01-interface essential/27-link:unlink/hyperlink-circle.svg",
            IconEventSpec(
                url=f"https://cdn-test.meya.ai/icon/streamline-regular/01-interface-essential/27-link-unlink/hyperlink-circle.svg"
            ),
        ),
        (
            "streamline-light/34-weather/02-day & night/day-sunrise.svg",
            IconEventSpec(
                url=f"https://cdn-test.meya.ai/icon/streamline-light/34-weather/02-day-night/day-sunrise.svg"
            ),
        ),
        (
            IconElementSpec(
                path="streamline-bold/16-files-folders/01-common-files/common-file-add.svg",
                color="blue",
            ),
            IconEventSpec(
                url=f"https://cdn-test.meya.ai/icon/streamline-bold/16-files-folders/01-common-files/common-file-add.svg",
                color="blue",
            ),
        ),
        (
            IconElementSpec(
                url="https://fonts.gstatic.com/s/i/materialicons/autorenew/v5/24px.svg"
            ),
            IconEventSpec(
                url="https://fonts.gstatic.com/s/i/materialicons/autorenew/v5/24px.svg"
            ),
        ),
    ],
)
def test_from_element_spec_union(
    icon_element_spec: Optional[IconElementSpecUnion],
    icon_event_spec: Optional[IconEventSpec],
):
    with patch_env():
        assert (
            IconEventSpec.from_element_spec(icon_element_spec)
            == icon_event_spec
        )
