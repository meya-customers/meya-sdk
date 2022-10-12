import hmac
import json

from base64 import b64encode
from collections import OrderedDict
from hashlib import sha1


def order_dict_by_keys(params: dict) -> OrderedDict:
    return OrderedDict(sorted(params.items()))


def concat_dict(data: OrderedDict) -> str:
    # TODO: support nested objects using recursive method
    return "".join([f"{key}{value}" for key, value in data.items()])


def convert_dict_to_string(data: dict) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def validate(
    api_key: str, url: str, data: dict, signature: str, delimiters: bool = True
) -> bool:
    fn = compute if delimiters else compute_no_delimiters
    return fn(api_key, url, data) == signature


def compute_no_delimiters(api_key: str, url: str, params: dict) -> str:
    param_string = concat_dict(order_dict_by_keys(params))
    return _compute(api_key, url + param_string)


def compute(api_key: str, url: str, data: dict) -> str:
    return _compute(api_key, url + convert_dict_to_string(data))


def _compute(api_key: str, data: str) -> str:
    hashed = hmac.new(api_key.encode("utf-8"), data.encode("utf-8"), sha1)
    return b64encode(hashed.digest()).decode("utf-8")
