import meya.util.uuid

from meya.util.sha1 import sha1_hex
from typing import Any


def generate_blob_id(ref_key_value: str):
    return f"blob-{ref_key_value}"


def generate_button_id() -> str:
    return f"b-{meya.util.uuid.uuid4_hex()}"


def generate_form_id() -> str:
    return f"form-{meya.util.uuid.uuid4_hex()}"


def generate_field_id() -> str:
    return f"f-{meya.util.uuid.uuid4_hex()}"


def generate_page_id() -> str:
    return f"p-{meya.util.uuid.uuid4_hex()}"


def generate_magic_link_id() -> str:
    return f"l-{meya.util.uuid.uuid4_hex()}"


def generate_thread_id() -> str:
    return f"t-{meya.util.uuid.uuid4_hex()}"


def generate_user_id() -> str:
    return f"u-{meya.util.uuid.uuid4_hex()}"


def generate_request_id(*data: Any) -> str:
    if data:
        return f"r-{sha1_hex(*data)}"
    else:
        return f"r-{meya.util.uuid.uuid4_hex()}"


def generate_trace_id() -> str:
    return f"tr-{meya.util.uuid.uuid4_hex()}"


def generate_orb_integration_user_id() -> str:
    return f"ou-{meya.util.uuid.uuid4_hex()}"


def generate_orb_integration_thread_id() -> str:
    return f"ot-{meya.util.uuid.uuid4_hex()}"


def generate_orb_session_token() -> str:
    return f"os-{meya.util.uuid.uuid4_hex()}"


def generate_log_query_id() -> str:
    return f"lq-{meya.util.uuid.uuid4_hex()}"


def generate_zendesk_chat_session_id() -> str:
    return f"zdcs-{meya.util.uuid.uuid4_hex()}"


def generate_webv1_integration_user_id() -> str:
    return f"webv1u-{meya.util.uuid.uuid4_hex()}"


def generate_webv1_session_token() -> str:
    return f"webv1s-{meya.util.uuid.uuid4_hex()}"


def generate_webv1_channel_id() -> str:
    return f"webv1c-{meya.util.uuid.uuid4_hex()}"
