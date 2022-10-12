from dataclasses import dataclass
from http import HTTPStatus
from meya.directly.component.api import DirectlyApiComponent
from meya.directly.component.understand.next import UnderstandResult
from meya.element.field import element_field
from meya.element.field import response_field
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import ApiComponentResponse


@dataclass
class UnderstandLabel(UnderstandResult):
    predicted_class: str = response_field()


@dataclass
class PredictResponse(ApiComponentResponse):
    predictive_routing: UnderstandLabel = response_field(default=None)
    intent_classifier: UnderstandLabel = response_field(default=None)
    intent_match: str = response_field(default="")

    def __post_init__(self):
        self.intent_match = self._intent_match

    @property
    def _intent_match(self) -> str:
        if not self.intent_classifier:
            return ""
        elif self.intent_classifier.is_confident:
            return self.intent_classifier.predicted_class
        else:
            return ""

    @classmethod
    def create(cls, res: HttpResponseEntry) -> "PredictResponse":
        ok = res.status == HTTPStatus.OK
        kwargs = {}
        if ok:
            for result in res.data["results"]:
                model_id = result["modelId"]
                if model_id in {"predictive_routing", "intent_classifier"}:
                    for label in result["labels"]:
                        kwargs[model_id] = UnderstandLabel(
                            predicted_class=label["predictedClass"],
                            confidence_score=label["confidenceScore"],
                            threshold=label["threshold"],
                        )
        return cls(result=res.data, status=res.status, ok=ok, **kwargs)


@dataclass
class DirectlyUnderstandPredictComponent(DirectlyApiComponent):
    text: str = element_field()

    @dataclass
    class Response(PredictResponse):
        pass

    async def make_request(self) -> HttpResponseEntry:
        return await self.api.understand_predict(text=self.text)

    def create_response(self, res: HttpResponseEntry) -> PredictResponse:
        return PredictResponse.create(res)
