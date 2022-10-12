import pytest

from meya.db.view.thread import ThreadMode
from meya.db.view.thread import ThreadView
from meya.thread.entry.data import ThreadDataEntry


def test_mode():
    mode = ThreadMode("agent")
    assert mode
    assert mode.agent
    assert not mode.user
    assert mode == "agent"


def test_mode_none():
    mode = ThreadMode(None)
    assert mode
    assert not mode.user
    assert mode != "agent"
    assert mode.bot


def test_thread_get():
    thread = ThreadView(id="t1", data={"k1": "v1", "k2": {"k3": "v2"}})
    assert thread.k0 is None
    assert thread.k2 == {"k3": "v2"}
    assert thread.k2 == {"k3": "v2"}
    thread.k1 = "v3"
    thread.k4 = "v4"
    assert thread.k0 is None
    assert thread.k1 == "v3"
    assert thread.k2 == {"k3": "v2"}
    assert thread.k4 == "v4"


def test_thread_invalid_get():
    thread = ThreadView(id="t1", data={"k1": "v1", "k2": {"k3": "v2"}})
    with pytest.raises(AttributeError) as excinfo:
        print(thread._protected)
    assert str(excinfo.value) == (
        "type object 'ThreadView' cannot get attribute '_protected'"
    )


def test_thread_invalid_set():
    thread = ThreadView(id="t1", data={"k1": "v1", "k2": {"k3": "v2"}})
    with pytest.raises(AttributeError) as excinfo:
        thread._protected = 0
    assert str(excinfo.value) == (
        "type object 'ThreadView' cannot set attribute '_protected'"
    )
    with pytest.raises(AttributeError) as excinfo:
        thread.changes = 0  # noqa
    assert str(excinfo.value) == (
        "type object 'ThreadView' cannot set attribute 'changes'"
    )
    with pytest.raises(AttributeError) as excinfo:
        thread.load = 0
    assert str(excinfo.value) == (
        "type object 'ThreadView' cannot set attribute 'load'"
    )


def test_simple_thread_changes():
    thread = ThreadView(id="t1", data={"k1": "v1"})
    thread.k2 = "v2"
    assert thread.changes == [
        ThreadDataEntry(thread_id="t1", key="k2", value="v2")
    ]
    thread.k1 = "v3"
    assert thread.changes == [
        ThreadDataEntry(thread_id="t1", key="k1", value="v3"),
        ThreadDataEntry(thread_id="t1", key="k2", value="v2"),
    ]


def test_complex_thread_changes():
    thread = ThreadView(id="t1", data={"k1": {"k2": "v1"}})
    thread.k3 = "v2"
    assert thread.changes == [
        ThreadDataEntry(thread_id="t1", key="k3", value="v2")
    ]
    thread = ThreadView(id="t1", data={"k1": {"k2": "v1"}})
    thread.k1["k2"] = "v3"
    assert thread.changes == [
        ThreadDataEntry(thread_id="t1", key="k1", value={"k2": "v3"})
    ]


def test_simple_thread_no_changes():
    thread = ThreadView(id="t1", data={"k1": "v1"})
    thread.k2 = "v2"
    thread.k2 = None
    assert thread.changes == []
    thread.k3 = None
    assert thread.changes == []
    thread.k1 = "v1"
    assert thread.changes == []


def test_complex_thread_no_changes():
    thread = ThreadView(id="t1", data={"k1": {"k2": "v1"}})
    thread.k3 = "v2"
    thread.k3 = None
    assert thread.changes == []
    thread.k4 = None
    assert thread.changes == []
    thread.k1["k2"] = "v1"
    assert thread.changes == []
