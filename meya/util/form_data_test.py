import pytest

from aiohttp import FormData
from meya.util.form_data import BinaryFile
from meya.util.form_data import parse_dict_as_form_data


@pytest.mark.parametrize(
    ("payload", "file_obj", "form_data"),
    [
        (
            {
                "body": "",
                "author_id": "author",
                "options": {"archive": False},
                "text": "text",
                "attachments": [
                    BinaryFile(
                        filename="blob-5cc.jpg",
                        content_type="image/jpeg",
                        data=b"",
                    )
                ],
            },
            {
                "attachments": [
                    BinaryFile(
                        filename="blob-5cc.jpg",
                        content_type="image/jpeg",
                        data=b"",
                    )
                ]
            },
            FormData(
                fields={
                    "body": "",
                    "author_id": "author",
                    "options[archive]": "false",
                    "text": "text",
                }
            ),
        ),
        (
            {
                "name": "name",
                "description": "description",
                "is_spammer": True,
                "handles": [
                    {
                        "handle": "meya_user/u-772c4bf2ada04bb59a2fc5bebd8c6344",
                        "source": "custom",
                    }
                ],
                "avatar": BinaryFile(
                    filename="Test", content_type="image", data=b""
                ),
            },
            {
                "avatar": BinaryFile(
                    filename="Test", content_type="image", data=b""
                )
            },
            FormData(
                fields={
                    "name": "name",
                    "description": "description",
                    "is_spammer": "true",
                    "handles[0][handle]": "meya_user/u-772c4bf2ada04bb59a2fc5bebd8c6344",
                    "handles[0][source]": "custom",
                }
            ),
        ),
    ],
)
def test_front_conversation_parse(payload, file_obj, form_data):
    if file_obj:
        for k, v in file_obj.items():
            if isinstance(v, list):
                for index, file in enumerate(v):
                    form_data.add_field(
                        f"{k}[{index}]",
                        filename=file.filename,
                        content_type=file.content_type,
                        value=file.data,
                    )
            elif isinstance(v, BinaryFile):
                form_data.add_field(
                    k,
                    filename=v.filename,
                    content_type=v.content_type,
                    value=v.data,
                )

    parsed_form_data = parse_dict_as_form_data(payload)
    for index, field in enumerate(parsed_form_data._fields):
        assert field == form_data._fields[index]
