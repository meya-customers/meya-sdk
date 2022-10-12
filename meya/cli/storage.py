from aiohttp import CookieJar
from appdirs import user_cache_dir
from dataclasses import dataclass
from dataclasses import field
from http.cookies import Morsel
from http.cookies import SimpleCookie
from meya.util.yaml import from_yaml
from meya.util.yaml import to_yaml
from os import chmod
from os import makedirs
from os import path
from typing import Dict
from typing import List
from typing import Optional
from typing import cast
from yarl import URL

CACHE_PATH = user_cache_dir("meya-sdk")
SESSION_PATH = path.join(CACHE_PATH, "session.txt")


@dataclass
class Storage:
    url: URL
    user_id: Optional[str] = field(init=False)
    all_user_ids: Dict[str, str] = field(init=False)
    unsafe: bool = field(init=False)
    cookie_jar: CookieJar = field(init=False)
    read_only_cookies: List[str] = field(init=False)

    def __post_init__(self):
        self.user_id = None
        self.all_user_ids = dict()
        self.unsafe = URL(self.url).scheme == "http"
        self.cookie_jar = CookieJar(unsafe=self.unsafe)
        self.read_only_cookies = list()
        makedirs(CACHE_PATH, exist_ok=True)
        chmod(CACHE_PATH, 0o700)

    def load(self):
        if path.exists(SESSION_PATH):
            with open(SESSION_PATH, "r") as session_file:
                session_data = from_yaml(session_file)
            self.all_user_ids = session_data["user_ids"]
            self.user_id = self.all_user_ids.get(str(self.url))
            self.cookie_jar.clear()
            self.read_only_cookies.clear()
            cookies = session_data["cookies"]
            for cookie in cookies:
                simple_cookie = SimpleCookie()
                simple_cookie.load(cookie)
                filter_jar = CookieJar(unsafe=self.unsafe)
                filter_jar.update_cookies(simple_cookie)
                if filter_jar.filter_cookies(URL(self.url)):
                    self.cookie_jar.update_cookies(simple_cookie)
                else:
                    self.read_only_cookies.append(cookie)

    def save(self):
        self.all_user_ids[str(self.url)] = self.user_id
        morsels = [cast(Morsel, morsel.copy()) for morsel in self.cookie_jar]
        for morsel in morsels:
            if morsel["max-age"]:
                # Convert to absolute expiry time
                morsel["expires"] = int(morsel["max-age"])
                del morsel["max-age"]
        cookies = [morsel.OutputString() for morsel in morsels]
        session_data = {
            "user_ids": self.all_user_ids,
            "cookies": cookies + self.read_only_cookies,
        }
        with open(SESSION_PATH, "w") as session_file:
            to_yaml(session_data, session_file)
