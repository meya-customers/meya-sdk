from dataclasses import dataclass
from typing import List
from typing import Optional


@dataclass
class Recipient:
    email: str
    name: Optional[str] = None

    @property
    def as_text(self) -> str:
        if self.name:
            return f"{self.name} <{self.email}>"
        else:
            return self.email

    @staticmethod
    def list_as_text(recipients: List["Recipient"]) -> List[str]:
        recipients = recipients or []
        return [recipient.as_text for recipient in recipients]
