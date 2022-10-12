from dataclasses import dataclass
from email_validator import EmailNotValidError
from email_validator import validate_email
from meya.element.field import response_field
from meya.text.trigger import TextTrigger
from meya.trigger.element import TriggerMatchResult
from typing import Optional


@dataclass
class EmailAddressTriggerResponse:
    result: str = response_field(sensitive=True, default="")


@dataclass
class EmailAddressTrigger(TextTrigger):
    async def match(self) -> TriggerMatchResult:
        result = self.validate_email(self.entry.text)
        if self.confidence is not None or result:
            confidence = self.confidence or self.MAX_CONFIDENCE
            return self.succeed(
                confidence=confidence,
                data=EmailAddressTriggerResponse(result=result or ""),
            )
        else:
            return self.fail()

    @staticmethod
    def validate_email(text: str) -> Optional[str]:
        try:
            valid = validate_email(text)
            return valid.email
        except EmailNotValidError:
            return None
