from typing import Tuple


def parse_front_request_client_token(bearer_token: str) -> Tuple[str, str]:
    meya_token = bearer_token.replace("Bearer ", "").split(":", 2)
    return meya_token[0], ("" if len(meya_token) == 1 else meya_token[1])
