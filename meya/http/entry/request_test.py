import pytest

from meya.element.element_test import create_http_request_entry
from meya.integration.element import Integration


@pytest.mark.parametrize(
    ("header", "expected_ip_address"),
    [
        (
            {
                "X-Forwarded-For": "127.0.0.1, 72.136.18.233, 34.107.135.48, 192.168.8.1"
            },
            "72.136.18.233",
        ),
        (
            {"X-Forwarded-For": "72.136.18.233, 34.107.135.48, 192.168.8.1"},
            "72.136.18.233",
        ),
        (
            {"x-forwarded-for": "72.136.18.233, 34.107.135.48, 192.168.8.1"},
            "72.136.18.233",
        ),
        ({"BOGUS": "bogus value"}, None),
        ({}, None),
    ],
)
def test_get_ip_address(header, expected_ip_address):
    integration = Integration(id="generic")
    request = create_http_request_entry(
        integration=integration, headers=header
    )
    ip_address = request.get_ip_address()
    assert ip_address == expected_ip_address
