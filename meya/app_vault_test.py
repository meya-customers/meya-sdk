from meya.app_vault import AppVault


def test_from_combined_keys():
    app_vault_dict = {
        "clearbit": "fake_clearbit_key",
        "mailgun.domain": "example.org",
        "mailgun.api_key": "fake_mailgun_key",
        "dialogflow.service_account_key": {
            "type": "service_account",
            "project_id": "example",
            "private_key_id": "fake_dialogflow_key_id",
        },
    }
    assert AppVault.from_combined_keys(app_vault_dict) == {
        "clearbit": "fake_clearbit_key",
        "mailgun": {"domain": "example.org", "api_key": "fake_mailgun_key"},
        "dialogflow": {
            "service_account_key": {
                "type": "service_account",
                "project_id": "example",
                "private_key_id": "fake_dialogflow_key_id",
            }
        },
    }


def test_overlapping_from_combined_keys():
    app_vault_dict = {
        "a0": {"a1": 1},
        "a0.a2": 2,
        "b0.b2": 3,
        "b0": {"b1": 4},
        "c0": 5,
        "c0.c1": 6,
        "d0.d1": 7,
        "d0": 8,
    }
    assert AppVault.from_combined_keys(app_vault_dict) == {
        "a0": {"a1": 1, "a2": 2},
        "b0": {"b1": 4, "b2": 3},
        "c0": {"c1": 6},
        "d0": {"d1": 7},
    }
