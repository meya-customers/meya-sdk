from dataclasses import dataclass
from http import HTTPStatus
from meya.directly.component.api import DirectlyApiComponent
from meya.element.field import element_field
from meya.element.field import response_field
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import ApiComponentResponse
from numbers import Real
from typing import Optional


@dataclass
class UnderstandResult:
    confidence_score: Real = response_field()
    threshold: Real = response_field()
    is_confident: bool = response_field(default=None)

    def __post_init__(self):
        self.is_confident = self._is_confident

    @property
    def _is_confident(self) -> bool:
        # on null pr model, proceed
        if self.confidence_score is None or self.threshold is None:
            return True
        else:
            return self.confidence_score >= self.threshold


@dataclass
class NextResponse(ApiComponentResponse):
    automate: UnderstandResult = response_field(default=None)
    engage: UnderstandResult = response_field(default=None)

    @classmethod
    def create(cls, res: HttpResponseEntry) -> "NextResponse":
        ok = res.status == HTTPStatus.OK
        kwargs = {}
        if ok:
            for result in res.data["results"]:
                name = result["name"]
                if name in {"automate", "engage"}:
                    kwargs[name] = UnderstandResult(
                        confidence_score=result["confidenceScore"],
                        threshold=result["threshold"],
                    )
        return cls(result=res.data, status=res.status, ok=ok, **kwargs)


@dataclass
class DirectlyUnderstandNextComponent(DirectlyApiComponent):
    text: str = element_field()
    language: Optional[str] = element_field(default=None)

    @dataclass
    class Response(NextResponse):
        pass

    async def make_request(self) -> HttpResponseEntry:
        return await self.api.understand_next(
            text=self.text, language=self.language
        )

    def create_response(self, res: HttpResponseEntry) -> NextResponse:
        return NextResponse.create(res)
