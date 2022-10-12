from dataclasses import dataclass
from meya.db.view.http import HttpTimeoutError
from meya.directly.component.automate.message import AutomateMessage
from meya.directly.component.understand.next import NextResponse
from meya.directly.component.understand.predict import PredictResponse
from meya.directly.integration import DirectlyIntegration
from meya.directly.integration import DirectlyIntegrationRef
from meya.element.field import element_field
from meya.element.field import response_field
from meya.integration.element.api import ApiComponentResponse
from meya.log.scope import Scope
from meya.text.trigger import TextTrigger
from meya.trigger.element import TriggerMatchResult
from meya.util.dict import to_dict
from typing import Optional


@dataclass
class DirectlyUnderstandTrigger(TextTrigger):
    integration: DirectlyIntegrationRef = element_field()
    language: Optional[str] = element_field(default=None)

    @dataclass
    class Response:
        question: str = response_field()

        # convenience response values
        engage: bool = response_field(default=False)
        intent: Optional[str] = response_field(default=None)
        answer: Optional[str] = response_field(default=None)
        answer_uuid: Optional[str] = response_field(default=None)

        # raw response objects
        next: NextResponse = response_field()
        predict: Optional[PredictResponse] = response_field(default=None)
        automate: Optional[AutomateMessage] = response_field(default=None)

        def compute(self):
            self.engage = self.next.engage.is_confident
            if self.predict:
                self.intent = self.predict.intent_match
            if self.automate:
                self.answer = self.automate.text
                self.answer_uuid = self.automate.answer_uuid

    async def match(self) -> TriggerMatchResult:
        integration: DirectlyIntegration = await self.resolve(self.integration)

        # understand/next
        try:
            next_ = NextResponse.create(
                await integration.api.understand_next(
                    text=self.entry.text, language=self.language
                )
            )
        except HttpTimeoutError:
            next_ = NextResponse.create_timeout()

        if not next_.ok:
            return self._api_error("understand_next", next_)
        response = self.Response(question=self.entry.text, next=next_)

        if next_.automate.is_confident:
            # understand/predict
            try:
                predict = PredictResponse.create(
                    await integration.api.understand_predict(
                        text=self.entry.text
                    )
                )
            except HttpTimeoutError:
                predict = PredictResponse.create_timeout()

            if not predict.ok:
                return self._api_error("understand_predict", predict)

            if predict.intent_match:
                response.predict = predict
                # automate/message
                try:
                    automate = AutomateMessage.create(
                        await integration.api.automate_post_message(
                            text=self.entry.text
                        )
                    )
                except HttpTimeoutError:
                    automate = AutomateMessage.create_timeout()

                if not automate.ok:
                    return self._api_error("automate_message", automate)

                response.automate = automate

        # compute convenient parameters
        response.compute()
        return self.succeed(data=response)

    def _api_error(
        self, method_name: str, response: ApiComponentResponse
    ) -> TriggerMatchResult:
        self.log.error(
            f"There was an error with Directly API: `{method_name}()`",
            self.entry,
            context=to_dict(response, preserve_nones=True),
            scope=Scope.BOT,
        )
        return self.fail()
