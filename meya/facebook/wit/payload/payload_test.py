from meya.facebook.wit.payload import WitIntent
from meya.facebook.wit.payload import WitMessageMeaningResponse


def test_message_meaning():
    assert WitMessageMeaningResponse.from_dict(
        {
            "text": "is going to rain tomorrow",
            "traits": {},
            "intents": [
                {
                    "id": "216622623546890",
                    "name": "wit$check_weather_condition",
                    "confidence": 0.999,
                }
            ],
            "entities": {
                "wit$datetime:datetime": [
                    {
                        "id": "853964465004660",
                        "end": 25,
                        "body": "tomorrow",
                        "name": "wit$datetime",
                        "role": "datetime",
                        "type": "value",
                        "grain": "day",
                        "start": 17,
                        "value": "2021-03-20T00:00:00.000-07:00",
                        "values": [
                            {
                                "type": "value",
                                "grain": "day",
                                "value": "2021-03-20T00:00:00.000-07:00",
                            }
                        ],
                        "entities": [],
                        "confidence": 1,
                    }
                ],
                "wit$age_of_person:age_of_person": [
                    {
                        "id": "853964465004660",
                        "end": 25,
                        "body": "tomorrow",
                        "name": "wit$datetime",
                        "role": "datetime",
                        "type": "value",
                        "grain": "day",
                        "start": 17,
                        "value": "2021-03-20T00:00:00.000-07:00",
                        "values": [
                            {
                                "type": "value",
                                "grain": "day",
                                "value": "2021-03-20T00:00:00.000-07:00",
                            }
                        ],
                        "entities": [],
                        "confidence": 1,
                    }
                ],
            },
        }
    ) == WitMessageMeaningResponse(
        text="is going to rain tomorrow",
        traits={},
        intents=[
            WitIntent(
                id="216622623546890",
                name="wit$check_weather_condition",
                confidence=0.999,
            )
        ],
        entities={
            "wit$datetime:datetime": [
                {
                    "id": "853964465004660",
                    "end": 25,
                    "body": "tomorrow",
                    "name": "wit$datetime",
                    "role": "datetime",
                    "type": "value",
                    "grain": "day",
                    "start": 17,
                    "value": "2021-03-20T00:00:00.000-07:00",
                    "values": [
                        {
                            "type": "value",
                            "grain": "day",
                            "value": "2021-03-20T00:00:00.000-07:00",
                        }
                    ],
                    "entities": [],
                    "confidence": 1,
                }
            ],
            "wit$age_of_person:age_of_person": [
                {
                    "id": "853964465004660",
                    "end": 25,
                    "body": "tomorrow",
                    "name": "wit$datetime",
                    "role": "datetime",
                    "type": "value",
                    "grain": "day",
                    "start": 17,
                    "value": "2021-03-20T00:00:00.000-07:00",
                    "values": [
                        {
                            "type": "value",
                            "grain": "day",
                            "value": "2021-03-20T00:00:00.000-07:00",
                        }
                    ],
                    "entities": [],
                    "confidence": 1,
                }
            ],
        },
    )
