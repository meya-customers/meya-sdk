from dataclasses import dataclass
from meya.http.payload import Payload
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class WebhookIdentity(Payload):
    id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    default_data: Optional[Dict[str, Any]] = None


@dataclass
class WebhookUser(WebhookIdentity):
    pass


@dataclass
class WebhookThread(WebhookIdentity):
    pass


@dataclass
class WebhookPayload(Payload):
    entry: Dict[str, Any]
    user: WebhookUser
    thread: WebhookThread
    integration_id: Optional[str] = None
    timestamp: Optional[int] = None
