from meya.db.view.user import UserView
from meya.user.entry.data import UserDataEntry


def test_user_get():
    user = UserView(id="u1", data={"k1": "v1", "k2": {"k3": "v2"}})
    assert user.k0 is None
    assert user.k2 == {"k3": "v2"}
    assert user.k2 == {"k3": "v2"}
    user.k1 = "v3"
    user.k4 = "v4"
    assert user.k0 is None
    assert user.k1 == "v3"
    assert user.k2 == {"k3": "v2"}
    assert user.k4 == "v4"


def test_simple_user_changes():
    user = UserView(id="u1", data={"k1": "v1"})
    user.k2 = "v2"
    assert user.changes == [UserDataEntry(user_id="u1", key="k2", value="v2")]
    user.k1 = "v3"
    assert user.changes == [
        UserDataEntry(user_id="u1", key="k1", value="v3"),
        UserDataEntry(user_id="u1", key="k2", value="v2"),
    ]


def test_complex_user_changes():
    user = UserView(id="u1", data={"k1": {"k2": "v1"}})
    user.k3 = "v2"
    assert user.changes == [UserDataEntry(user_id="u1", key="k3", value="v2")]
    user = UserView(id="u1", data={"k1": {"k2": "v1"}})
    user.k1["k2"] = "v3"
    assert user.changes == [
        UserDataEntry(user_id="u1", key="k1", value={"k2": "v3"})
    ]


def test_simple_user_no_changes():
    user = UserView(id="u1", data={"k1": "v1"})
    user.k2 = "v2"
    user.k2 = None
    assert user.changes == []
    user.k3 = None
    assert user.changes == []
    user.k1 = "v1"
    assert user.changes == []


def test_complex_user_no_changes():
    user = UserView(id="u1", data={"k1": {"k2": "v1"}})
    user.k3 = "v2"
    user.k3 = None
    assert user.changes == []
    user.k4 = None
    assert user.changes == []
    user.k1["k2"] = "v1"
    assert user.changes == []
