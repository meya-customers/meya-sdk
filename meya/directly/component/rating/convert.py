from dataclasses import dataclass
from meya.component.element import Component
from meya.directly.integration.api import Rating
from meya.element.field import element_field
from meya.entry import Entry
from meya.tile.component.rating import RatingType
from typing import List

RATING_MAP = {
    RatingType.STARS: {
        1: Rating.NEGATIVE_5,
        2: Rating.NEUTRAL_NEGATIVE_5,
        3: Rating.NEUTRAL_5,
        4: Rating.NEUTRAL_POSITIVE_5,
        5: Rating.POSITIVE_5,
    }
}


@dataclass
class RatingConvertComponent(Component):
    score: int = element_field()
    rating: RatingType = element_field()

    @dataclass
    class Response:
        result: Rating

    def validate(self):
        super().validate()
        types = ", ".join([key.value for key in RATING_MAP])
        if not (self.rating in RATING_MAP):
            raise self.validation_error(f"Rating must be one of {types}")
        scores = ", ".join([str(key) for key in RATING_MAP[self.rating]])
        if not (self.score in RATING_MAP[self.rating]):
            raise self.validation_error(f"Score must be one of {scores}")

    async def start(self) -> List[Entry]:
        response = self.Response(result=RATING_MAP[self.rating][self.score])
        return self.respond(data=response)
