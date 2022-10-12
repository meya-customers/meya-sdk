import pytest

from meya.tile.component.rating import RatingComponent
from meya.tile.component.rating import RatingType
from numbers import Real
from typing import List

TITLE = "How did you enjoy your experience?"


@pytest.mark.parametrize(
    ("rating", "result"),
    [
        (RatingType.FACES, [-2, -1, 0, 1, 2]),
        (RatingType.STARS, [1, 2, 3, 4, 5]),
        (RatingType.THUMBS, [-1, 1]),
    ],
)
@pytest.mark.asyncio
async def test_option_scores(rating: RatingType, result: List[Real]):
    component = RatingComponent(title=TITLE, rating=rating)
    for index, score in enumerate(result):
        assert component.rating.options[index].score == score
