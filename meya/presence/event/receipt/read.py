from dataclasses import dataclass
from meya.presence.event.receipt import ReceiptEvent


@dataclass
class ReadReceiptEvent(ReceiptEvent):
    pass
