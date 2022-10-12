from dataclasses import dataclass
from markdownify import markdownify as md
from meya.component.element.interactive import InteractiveComponent
from meya.core.meta_level import MetaLevel
from meya.element.field import element_field
from meya.element.field import meta_field
from meya.email.event.event import EmailEvent
from meya.entry import Entry
from typing import List
from typing import Optional


@dataclass
class EmailComponent(InteractiveComponent):
    extra_alias: str = meta_field(value="email")

    message_id: Optional[str] = element_field(
        default=None,
        help="Identifies the email using the Message-ID header",
        level=MetaLevel.ADVANCED,
    )
    html: Optional[str] = element_field(
        default=None, help="HTML body content of the email"
    )
    text: Optional[str] = element_field(
        default=None, help="Text body content of the email"
    )
    subject: Optional[str] = element_field(
        default=None, help="Subject of the email"
    )

    async def start(self) -> List[Entry]:
        return self.respond(
            EmailEvent(
                message_id=self.message_id,
                html=self.html,
                text=self.text,
                subject=self.subject,
            )
        )

    def validate(self):
        super().validate()
        if not self.html and not self.text:
            raise self.validation_error(
                "Both `html` and `text` can't be empty"
            )
        if not self.text:
            self.text = md(self.html)
