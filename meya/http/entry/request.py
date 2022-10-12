from dataclasses import dataclass
from meya.entry.field import entry_field
from meya.http.direction import Direction
from meya.http.entry import HttpEntry
from numbers import Real
from typing import Any
from typing import Dict
from typing import Optional


@dataclass
class HttpRequestEntry(HttpEntry):
    allow_redirects: Optional[bool] = entry_field(default=None)
    app_id: Optional[str] = entry_field(default=None)
    content_type: Optional[str] = entry_field(default=None)
    cookies: Dict[str, str] = entry_field(default_factory=dict, sensitive=True)
    data: Optional[Dict[str, Any]] = entry_field(default=None, sensitive=True)
    direction: Direction = entry_field()
    headers: Dict[str, str] = entry_field(default_factory=dict, sensitive=True)
    integration_id: Optional[str] = entry_field(default=None)
    integration_name: Optional[str] = entry_field(default=None)
    method: str = entry_field()
    params: Dict[str, str] = entry_field(default_factory=dict, sensitive=True)
    text: Optional[str] = entry_field(default=None, sensitive=True)
    timeout: Optional[Real] = entry_field(default=None)
    url: str = entry_field()
    error: Optional[str] = entry_field(default=None)

    def get_header(
        self, name: str, default: Optional[str] = None
    ) -> Optional[str]:
        from multidict import CIMultiDict

        return CIMultiDict(self.headers).get(name, default)

    def get_accept_language_header(
        self, default: Optional[str] = None
    ) -> Optional[str]:
        return self.get_header("accept-language", default)

    def get_best_accept_language(self) -> Optional[str]:
        from werkzeug.datastructures import LanguageAccept
        from werkzeug.http import parse_accept_header

        accept_language = parse_accept_header(
            self.get_accept_language_header(), LanguageAccept
        )
        # TODO Use best_match with app-supported languages (config.yaml)
        best_language = accept_language.best
        if best_language:
            return best_language
        else:
            return None

    def get_ip_address(self) -> Optional[str]:
        ip_address = None
        ip_addresses = self.get_header("x-forwarded-for", "").split(",")
        for ip in ip_addresses:
            if not ip or ip.startswith("127"):
                continue
            else:
                ip_address = ip.strip()
                break
        return ip_address
