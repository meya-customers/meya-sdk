from dataclasses import dataclass
from dataclasses import field
from meya.db.view.http import HttpBasicAuth
from meya.http.entry.response import HttpResponseEntry
from meya.integration.element.api import Api
from typing import Optional

API_ROOT = "https://person-stream.clearbit.com/v2"


@dataclass
class ClearbitEnrichedEmail:
    email: str
    company: Optional[dict] = field(default_factory=dict)
    person: Optional[dict] = field(default_factory=dict)

    @property
    def is_enriched(self) -> bool:
        return bool(self.company) or bool(self.person)


@dataclass
class ClearbitApi(Api):
    api_key: str
    api_root: str = API_ROOT

    async def enrich(self, email: str) -> HttpResponseEntry:
        return await self.http.get(
            f"{self.api_root}/combined/find",
            params=dict(email=email),
            auth=self.auth,
        )

    @property
    def auth(self) -> HttpBasicAuth:
        return HttpBasicAuth(self.api_key, "")
