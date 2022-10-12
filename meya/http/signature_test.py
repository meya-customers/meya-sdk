import pytest

from meya.http.signature import compute
from meya.http.signature import convert_dict_to_string
from meya.http.signature import validate


def test_signature_no_delimeters():
    """
    See https://www.twilio.com/docs/usage/security#validating-requests
    """
    auth_token = "12345"
    url = "https://mycompany.com/myapp.php?foo=1&bar=2"
    params = {
        "CallSid": "CA1234567890ABCDE",
        "Caller": "+14158675309",
        "Digits": "1234",
        "From": "+14158675309",
        "To": "+18005551212",
    }

    # The X-Twilio-Signature header attached to the request
    twilio_signature = "RSOYDt4T1cUTdK1PDd93/VVr8B8="
    assert validate(
        auth_token, url, params, twilio_signature, delimiters=False
    )


def test_signature_with_delimiters():
    api_key = "123465456"
    postback_url = "https://grid.meya.ai"
    data = {
        "user": {"id": 123},
        "event": {"type": "type", "data": {"pi": 0.314}},
    }
    assert (
        compute(api_key, postback_url, data) == "qvQcbl6MoBdcxix5mxA8h6ZsnbA="
    )


@pytest.mark.parametrize(
    ("data", "data_as_str"),
    [
        ({"foo": "bar"}, '{"foo":"bar"}'),
        ({"b": 1, "a": None}, '{"a":null,"b":1}'),
        ({"b": 1, "a": {"e": 0, "d": 1}}, '{"a":{"d":1,"e":0},"b":1}'),
    ],
)
def test_convert_dict_to_string(data: dict, data_as_str: str):
    assert convert_dict_to_string(data) == data_as_str
